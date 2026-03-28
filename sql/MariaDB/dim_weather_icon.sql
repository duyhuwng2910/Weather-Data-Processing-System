-- ============================================================
-- Table: dim_weather_icon
-- ============================================================
create table if not exists dim_weather_icon (
    id VARCHAR(10) PRIMARY KEY,
    type VARCHAR(10),
    description VARCHAR(255)
)
;

-- ============================================================
-- INSERT statements for table: dim_weather_icon
-- Fields: id (png filename without extension), type (day/night), description
-- Source: https://openweathermap.org/weather-conditions
-- ============================================================

INSERT INTO dim_weather_icon (id, type, description) VALUES
-- Clear sky
('01d', 'day',   'clear sky'),
('01n', 'night', 'clear sky'),

-- Few clouds
('02d', 'day',   'few clouds'),
('02n', 'night', 'few clouds'),

-- Scattered clouds
('03d', 'day',   'scattered clouds'),
('03n', 'night', 'scattered clouds'),

-- Broken clouds
('04d', 'day',   'broken clouds'),
('04n', 'night', 'broken clouds'),

-- Shower rain
('09d', 'day',   'shower rain'),
('09n', 'night', 'shower rain'),

-- Rain
('10d', 'day',   'rain'),
('10n', 'night', 'rain'),

-- Thunderstorm
('11d', 'day',   'thunderstorm'),
('11n', 'night', 'thunderstorm'),

-- Snow
('13d', 'day',   'snow'),
('13n', 'night', 'snow'),

-- Mist / Atmosphere
('50d', 'day',   'mist'),
('50n', 'night', 'mist');
