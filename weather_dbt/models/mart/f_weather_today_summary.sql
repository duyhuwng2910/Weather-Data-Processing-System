{{
    config(
        materialized='table'
    )
}}


with
summary as (
    select
         city_id

        ,count(*)                           as total_records

        ,round(avg(temp), 1)                as avg_temp
        ,round(min(temp), 1)                as min_temp
        ,round(max(temp), 1)                as max_temp
        ,round(max(temp) - min(temp), 1)    as temp_range

        ,round(avg(feels_like), 1)          as avg_feels_like
        ,round(min(feels_like), 1)          as min_feels_like
        ,round(max(feels_like), 1)          as max_feels_like

        ,round(avg(humidity), 1)            as avg_humidity
        ,round(min(humidity), 1)            as min_humidity
        ,round(max(humidity), 1)            as max_humidity

        ,round(avg(wind_speed), 1)          as avg_wind_speed
        ,round(max(wind_speed), 1)          as max_wind_speed
        ,round(max(wind_gust), 1)           as max_wind_gust

        ,round(avg(visibility), 1)          as avg_visibility
        ,round(min(visibility), 1)          as min_visibility

        ,round(avg(pressure), 1)            as avg_pressure

        ,min(event_date)                    as event_date
        ,min(event_hour)                    as start_hour
        ,max(event_hour)                    as latest_hour

    from {{ ref('f_weather_hourly') }}
    where event_date = date(convert_tz(current_timestamp(), '+00:00', '+07:00'))
    group by city_id
)
select *
from summary
