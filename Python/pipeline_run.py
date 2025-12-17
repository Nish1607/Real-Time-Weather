
import requests
import pyodbc
from datetime import datetime
from Config import API_KEY, BASE_URL_FORECAST, FORECAST_DAYS, REQUEST_TIMEOUT, CONN_STR


def fetch_forecast_payload(city_name: str) -> dict:
    """
    Calls WeatherAPI forecast endpoint for a single city.
    Returns JSON payload with: location, current (with air_quality), forecast (hourly), alerts
    """
    params = {
        "key": API_KEY,
        "q": f"{city_name},Canada",
        "days": FORECAST_DAYS,
        "aqi": "yes",
        "alerts": "yes",
    }
    r = requests.get(BASE_URL_FORECAST, params=params, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    return r.json()


def parse_dt(dt_str: str) -> datetime:
    """
    WeatherAPI uses 'YYYY-MM-DD HH:MM'
    """
    return datetime.strptime(dt_str, "%Y-%m-%d %H:%M")


def get_active_cities(cursor) -> list[tuple[int, str]]:
    """
    Returns list of (CityId, CityName) from dim_city
    """
    cursor.execute("SELECT CityId, CityName FROM dbo.dim_city WHERE IsActive = 1 ORDER BY CityId;")
    return [(row.CityId, row.CityName) for row in cursor.fetchall()]


def insert_current_weather(cursor, city_id: int, observed_at: datetime, cur: dict, astro: dict):
    condition = cur.get("condition") or {}
    condition_text = condition.get("text")
    condition_icon = condition.get("icon")

    last_updated = parse_dt(cur.get("last_updated"))
    sunrise = (astro or {}).get("sunrise")
    sunset = (astro or {}).get("sunset")

    cursor.execute(
        """
        INSERT INTO dbo.fact_weather_current
        (
            CityId, ObservedAt, LastUpdated,
            TempC, FeelsLikeC, Humidity, WindKph, PressureMb,
            ConditionText, ConditionIcon,
            Sunrise, Sunset, vis_km, uv, wind_dir
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
        (
            city_id,
            observed_at,
            last_updated,
            cur.get("temp_c"),
            cur.get("feelslike_c"),
            cur.get("humidity"),
            cur.get("wind_kph"),
            cur.get("pressure_mb"),
            condition_text,
            condition_icon,
            sunrise,
            sunset,
            cur.get("vis_km"),
            cur.get("uv"),
            cur.get("wind_dir"),
        ),
    )


def insert_current_aqi(cursor, city_id: int, observed_at: datetime, cur: dict):
    aq = cur.get("air_quality") or {}

    cursor.execute(
        """
        INSERT INTO dbo.fact_air_quality_current
        (CityId, ObservedAt, CO, NO2, O3, SO2, PM2_5, PM10, US_EPA_Index, GB_DEFRA_Index)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
        (
            city_id,
            observed_at,
            aq.get("co"),
            aq.get("no2"),
            aq.get("o3"),
            aq.get("so2"),
            aq.get("pm2_5"),
            aq.get("pm10"),
            aq.get("us-epa-index"),
            aq.get("gb-defra-index"),
        ),
    )


def insert_hourly_forecast(cursor, city_id: int, forecast: dict):
    forecast_days = (forecast.get("forecastday") or [])
    for day in forecast_days:
        astro = day.get("astro") or {}
        sunrise = astro.get("sunrise")
        sunset = astro.get("sunset")

        hours = day.get("hour") or []
        for h in hours:
            time_text = h.get("time")
            forecast_at = parse_dt(time_text)
            last_updated = forecast_at

            condition = h.get("condition") or {}
            condition_text = condition.get("text")
            condition_icon = condition.get("icon")

            try:
                cursor.execute(
                    """
                    INSERT INTO dbo.fact_weather_forecast_hourly
                    (
                        CityId, ForecastAt, TimeText, LastUpdated,
                        TempC, Humidity, WindKph, ChanceOfRain,
                        ConditionText, ConditionIcon,
                        Sunrise, Sunset, vis_km, uv, wind_dir
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        city_id,
                        forecast_at,
                        time_text,
                        last_updated,
                        h.get("temp_c"),
                        h.get("humidity"),
                        h.get("wind_kph"),
                        h.get("chance_of_rain"),
                        condition_text,
                        condition_icon,
                        sunrise,
                        sunset,
                        h.get("vis_km"),
                        h.get("uv"),
                        h.get("wind_dir"),
                    ),
                )
            except pyodbc.IntegrityError:
                pass


def run_pipeline():
    conn = pyodbc.connect(CONN_STR)
    conn.autocommit = False
    cursor = conn.cursor()

    start_time = datetime.now()
    print("=" * 60)
    print(f"PIPELINE STARTED AT: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    cities = get_active_cities(cursor)
    success = 0
    failed = 0

    for city_id, city_name in cities:
        try:
            payload = fetch_forecast_payload(city_name)

            cur = payload["current"]
            observed_at = parse_dt(cur["last_updated"])

            astro_today = (
                payload.get("forecast", {})
                       .get("forecastday", [{}])[0]
                       .get("astro", {})
            )

            # Current Weather (skip duplicates)
            try:
                insert_current_weather(cursor, city_id, observed_at, cur, astro_today)
            except pyodbc.IntegrityError:
                pass

            # Current AQI (skip duplicates)
            try:
                insert_current_aqi(cursor, city_id, observed_at, cur)
            except pyodbc.IntegrityError:
                pass

            # Hourly Forecast (skip duplicates)
            try:
                insert_hourly_forecast(cursor, city_id, payload.get("forecast") or {})
            except pyodbc.IntegrityError:
                pass

            conn.commit()
            success += 1
            print(f"[OK] {city_name}")

        except Exception as e:
            conn.rollback()
            failed += 1
            print(f"[FAIL] {city_name}: {e}")

    cursor.close()
    conn.close()

    end_time = datetime.now()
    print("=" * 60)
    print(f"PIPELINE FINISHED AT: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"TOTAL DURATION: {(end_time - start_time)}")
    print(f"SUCCESS={success}, FAILED={failed}")
    print("=" * 60)

if __name__ == "__main__":
    run_pipeline()
