-- create database
create database if not exists weather_data;


-- create tables

-- raw table to store the data as it is ingested from the API, without any transformations or cleaning
create table if not exists weather_raw (
    lat FLOAT,
    lon FLOAT,
    weather_main VARCHAR(100),
    weather_description VARCHAR(255),
    weather_icon VARCHAR(20),
    temp FLOAT,
    feels_like FLOAT,
    temp_min FLOAT,
    temp_max FLOAT,
    pressure INT,
    humidity INT,
    visibility INT,
    wind_speed FLOAT,
    wind_deg INT,
    wind_gust FLOAT,
    clouds_all INT,
    city_id BIGINT,
    event_ts TIMESTAMP,
    ingest_ts TIMESTAMP
)
;

alter table weather_raw
add column if not exists weather_id INT after lon
;
