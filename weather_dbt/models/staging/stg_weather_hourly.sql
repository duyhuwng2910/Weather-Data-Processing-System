-- models/staging/stg_weather_hourly.sql

{{
    config(
        materialized='table'
    )
}}

with
source as (
    select *
    from {{ source('weather_data', 'weather_raw') }}
    where date(convert_tz(ingest_ts, '+00:00', '+07:00')) = date(convert_tz(current_timestamp(), '+00:00', '+07:00'))
),
cleaned as (
    select
         city_id

        ,weather_id
        ,weather_main
        ,weather_description
        ,weather_icon

        ,temp
        ,feels_like
        ,temp_min
        ,temp_max
        ,pressure
        ,humidity
        ,visibility

        ,wind_speed
        ,wind_deg
        ,wind_gust
        ,clouds_all

        ,convert_tz(event_ts, '+00:00', '+07:00')   as event_ts
        ,convert_tz(ingest_ts, '+00:00', '+07:00')  as ingest_ts

        ,date(convert_tz(event_ts, '+00:00', '+07:00'))  as event_date
        ,hour(convert_tz(event_ts, '+00:00', '+07:00'))  as event_hour
    from source
)
select *
from cleaned
