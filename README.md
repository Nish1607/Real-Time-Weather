

---

# 🌦️ Real-Time Weather & Air Quality Insights Dashboard (Power BI + Python + SQL)

This project presents a **Real-Time Weather & Air Quality Analytics Dashboard** built using **Power BI, Python, and SQL Server**. It ingests live weather and air quality data via APIs for **major GTA cities**, automates data pipelines, and visualizes actionable insights to support real-time, data-driven decisions.

---

## 🚀 Objective

To build an end-to-end **real-time analytics solution** that captures current weather conditions, air quality metrics, and short-term forecasts. The project focuses on **API integration, automated ETL pipelines, data validation, time-based aggregation, and interactive dashboards** to monitor weather trends and environmental conditions across the GTA.

---
## 🏗️ System Architecture & Data Flow

WeatherAPI
   ↓
Python ETL Pipeline
   ↓
SQL Server (Fact & Dimension Tables)
   ↓
Power BI Dashboard

## 🌆 Cities Covered (GTA)

Toronto, Mississauga, Brampton, Markham, Vaughan,
Richmond Hill, Oakville, Burlington, Ajax, Pickering, Scarborough


## 📁 Dataset Summary

The dataset is sourced from **WeatherAPI (live API)** and includes:

* Current weather conditions
* Hourly weather forecasts
* Air quality measurements (pollutants & indices)

Data is refreshed automatically and stored in SQL Server, simulating a **real-world streaming / near-real-time dataset** with changing values over time.

---

## 🗄️ Database Design

The data is stored in SQL Server using a star-schema inspired design.

## Dimension Table

dim_city – City metadata and active status

## Fact Tables

fact_weather_current – Current weather snapshot

fact_weather_forecast_hourly – Hourly forecast data

fact_air_quality_current – Current air quality metrics

Hourly forecast data is aggregated to daily level in Power BI using DAX.

## 🧹 Data Cleaning & Validation

Performed using **Python and SQL Server** to ensure accuracy, consistency, and analytical readiness.

Key steps included:

* Validating numeric ranges (temperature, wind speed, visibility, AQI metrics)
* Handling missing or null API responses safely
* Converting hourly timestamps into date-based aggregations
* Preventing duplicate inserts using primary & unique constraints
* Standardizing units (°C, km/h, km, hPa)
* Separating descriptive vs numeric fields for proper data modeling

### Key columns include:

* **CityId, ForecastAt, ObservedAt**
* **TempC, FeelsLikeC, WindKph, Humidity**
* **VisibilityKm, PressureMb, UV**
* **PM2.5, PM10, CO, NO2, SO2, O3**
* **ConditionText, ConditionIcon**
* **Sunrise, Sunset**

---

## 📌 Key KPIs and Visualizations

| KPI                           | Description                                | Visualization Type |
| ----------------------------- | ------------------------------------------ | ------------------ |
| 🌡️ Avg Temperature (°C)      | Daily average temperature from hourly data | KPI Card           |
| 🤗 Feels Like (°C)            | Average perceived temperature              | KPI Card           |
| 🌬️ Avg Wind Speed (km/h)     | Daily average wind speed                   | KPI Card           |
| 👁️ Avg Visibility (km)       | Average visibility conditions              | KPI Card           |
| 🌫️ Avg Pressure (hPa)        | Mean atmospheric pressure                  | KPI Card           |
| ☀️ UV Index                   | Average UV exposure level                  | KPI Card           |
| 📈 7-Day Temperature Forecast | Daily avg temperature trend                | Line Chart         |
| 🌧️ Max Chance of Rain (%)    | Highest rain probability per day           | Column Chart       |
| 🏭 Air Quality Breakdown      | PM2.5, PM10, CO, NO2, SO2, O3              | Bar / KPI Cards    |
| 🚦 AQI Index                  | Overall air quality severity               | KPI Card           |
| 🌅 Sunrise & Sunset           | Daily solar timings                        | Text Cards         |
| 🕒 Last Updated               | Latest data refresh timestamp              | KPI Card           |

---

## 🧮 Tools & Technologies

* **WeatherAPI** → Real-time data source (Current, Forecast, AQI)
* **Python (requests, pandas, pyodbc)** → API ingestion, transformation, automation
* **SQL Server** → Data storage, constraints, validation
* **Power BI** → Data modeling, DAX, interactive dashboards
* **DAX** → Time-based measures, averages, filters
* **Windows Task Scheduler** → Automated pipeline execution


---

## 🧠 Key Insights

* Clear daily temperature trends derived from **hourly forecast aggregation**
* Wind speed and visibility provide realistic comfort indicators
* AQI metrics highlight **pollution exposure variations across GTA cities**
* Consolidated dashboard enables **real-time situational awareness**
* Automated pipeline ensures **fresh data without manual intervention**

---

## 📸 Dashboard Preview
<img width="1659" height="922" alt="Screenshot 2025-12-16 190554" src="https://github.com/user-attachments/assets/ba4e5272-4b12-410f-9feb-3a4273d921ba" />


  
<img width="1641" height="917" alt="Screenshot 2025-12-16 190631" src="https://github.com/user-attachments/assets/bf301bb8-713f-4c67-8203-6b30cdb3d6b3" />


Example views:

* Real-time weather snapshot
* 6-day forecast trend
* Air quality & pollutant breakdown
* City-level comparisons
  
## Current Limitations

* Pipeline runs locally and requires the machine to be ON
* Forecast range limited by API plan
* Historical weather trend analysis not included

## Future Enhancements

## 🚀 Future Enhancements

* **Cloud scheduling** using Airflow or Azure Data Factory to replace local task scheduling
* **Power BI Service deployment** with On-Premises Data Gateway for automated dataset refresh
* **Historical trend analysis & anomaly detection** to identify unusual weather or air quality patterns
* *Weather alerts & AQI health recommendations** for proactive environmental awareness


---

## 🔁 Automation & Deployment

* Python ETL pipeline runs on a defined schedule using Windows Task Scheduler
* Weather data is fetched from APIs and stored in SQL Server
* Power BI Desktop connects directly to SQL Server*Dashboard refreshes reflect the latest ingested data

---

## ✅ Conclusion

The **Real-Time Weather & Air Quality Insights Dashboard** demonstrates a complete analytics workflow — from **live API ingestion and automated ETL pipelines** to **data modeling and interactive BI reporting**.This project highlights skills in **data engineering, SQL, Python automation, DAX, and Power BI**, and reflects real-world practices used in production analytics environments.

---
## 📬 Contact

**Nishi Patel**  
Data Analyst | SQL • Python • Power BI  

🔗 LinkedIn: www.linkedin.com/in/nishipatel09

🔗 GitHub: https://github.com/Nish1607 


