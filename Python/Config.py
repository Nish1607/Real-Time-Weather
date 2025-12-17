

# ---------- WEATHERAPI ----------
API_KEY = "bd5fc86fcae4480c83c145233251612" 

BASE_URL_CURRENT = "https://api.weatherapi.com/v1/current.json"
BASE_URL_FORECAST = "https://api.weatherapi.com/v1/forecast.json"

AQI = "yes"
ALERTS = "yes"
FORECAST_DAYS = 7

CITIES = [
    "Toronto,Canada",
    "Mississauga,Canada",
    "Brampton,Canada",
    "Markham,Canada",
    "Scarborough,Canada",
    "Richmond Hill,Canada",
    "Oakville,Canada",
    "Burlington,Canada",
    "Ajax,Canada",
    "Pickering,Canada",
    "Vaughan,Canada"
]

# ---------- SQL SERVER ----------
DB_NAME = "WeatherAQI_GTA"
SERVER = "NISHISONI\\SQLEXPRESS"

CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=NISHISONI\\SQLEXPRESS;"
    "DATABASE=WeatherAQI_GTA;"
    "Trusted_Connection=yes;"
)


REQUEST_TIMEOUT = 30
