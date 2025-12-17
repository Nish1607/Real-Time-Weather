-- 1) Create DB
IF DB_ID('WeatherAQI_GTA') IS NULL
BEGIN
  CREATE DATABASE WeatherAQI_GTA;
END
GO

USE WeatherAQI_GTA;
GO

-- 2) dim_city
IF OBJECT_ID('dbo.dim_city', 'U') IS NOT NULL DROP TABLE dbo.dim_city;
GO

CREATE TABLE dbo.dim_city (
  CityId     INT IDENTITY(1,1) PRIMARY KEY,
  CityName   VARCHAR(100) NOT NULL,
  Region     VARCHAR(50)  NOT NULL DEFAULT('GTA'),
  Country    VARCHAR(50)  NOT NULL DEFAULT('Canada'),
  IsActive   BIT NOT NULL DEFAULT(1),
  CreatedAt  DATETIME2(0) NOT NULL DEFAULT SYSUTCDATETIME()
);
GO

-- 3) fact_weather_current
IF OBJECT_ID('dbo.fact_weather_current', 'U') IS NOT NULL DROP TABLE dbo.fact_weather_current;
GO

CREATE TABLE dbo.fact_weather_current (
  CityId        INT NOT NULL,
  ObservedAt    DATETIME2(0) NOT NULL,  -- from current.last_updated (local time from API)
  TempC         DECIMAL(6,2) NULL,
  FeelsLikeC    DECIMAL(6,2) NULL,
  Humidity      INT NULL,
  WindKph       DECIMAL(6,2) NULL,
  PressureMb    INT NULL,
  ConditionText VARCHAR(200) NULL,
  InsertedAt    DATETIME2(0) NOT NULL DEFAULT SYSUTCDATETIME(),
  CONSTRAINT FK_weather_city FOREIGN KEY (CityId) REFERENCES dbo.dim_city(CityId),
  CONSTRAINT UQ_weather_city_time UNIQUE (CityId, ObservedAt)
);
GO

-- 4) fact_air_quality_current
IF OBJECT_ID('dbo.fact_air_quality_current', 'U') IS NOT NULL DROP TABLE dbo.fact_air_quality_current;
GO

CREATE TABLE dbo.fact_air_quality_current (
  CityId         INT NOT NULL,
  ObservedAt     DATETIME2(0) NOT NULL,  -- same as weather ObservedAt
  CO             DECIMAL(10,2) NULL,
  NO2            DECIMAL(10,2) NULL,
  O3             DECIMAL(10,2) NULL,
  SO2            DECIMAL(10,2) NULL,
  PM2_5          DECIMAL(10,2) NULL,
  PM10           DECIMAL(10,2) NULL,
  US_EPA_Index   INT NULL,
  GB_DEFRA_Index INT NULL,
  InsertedAt     DATETIME2(0) NOT NULL DEFAULT SYSUTCDATETIME(),
  CONSTRAINT FK_aqi_city FOREIGN KEY (CityId) REFERENCES dbo.dim_city(CityId),
  CONSTRAINT UQ_aqi_city_time UNIQUE (CityId, ObservedAt)
);
GO

-- 5) fact_weather_forecast_hourly (recommended)
IF OBJECT_ID('dbo.fact_weather_forecast_hourly', 'U') IS NOT NULL DROP TABLE dbo.fact_weather_forecast_hourly;
GO

CREATE TABLE dbo.fact_weather_forecast_hourly (
  CityId        INT NOT NULL,
  ForecastAt    DATETIME2(0) NOT NULL,  -- from forecastday.hour.time
  TempC         DECIMAL(6,2) NULL,
  Humidity      INT NULL,
  WindKph       DECIMAL(6,2) NULL,
  ChanceOfRain  INT NULL,
  ConditionText VARCHAR(200) NULL,
  InsertedAt    DATETIME2(0) NOT NULL DEFAULT SYSUTCDATETIME(),
  CONSTRAINT FK_fcst_city FOREIGN KEY (CityId) REFERENCES dbo.dim_city(CityId),
  CONSTRAINT UQ_fcst_city_time UNIQUE (CityId, ForecastAt)
);
GO



