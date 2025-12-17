USE WeatherAQI_GTA;
GO

TRUNCATE TABLE dbo.dim_city;

INSERT INTO dbo.dim_city (CityName, Region, Country)
VALUES
('Toronto','GTA','Canada'),
('Mississauga','GTA','Canada'),
('Brampton','GTA','Canada'),
('Markham','GTA','Canada'),
('Vaughan','GTA','Canada'),
('Richmond Hill','GTA','Canada'),
('Oakville','GTA','Canada'),
('Burlington','GTA','Canada'),
('Ajax','GTA','Canada'),
('Pickering','GTA','Canada');
GO
