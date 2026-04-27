{{
    config(
        materialized='incremental',
        unique_key=['city_id', 'ingest_ts']
    )
}}

with
stg_data as (
    select *
    from {{ ref('stg_weather_hourly') }}
)
select
     s.city_id
    ,dc.name as city_name

    ,s.weather_id
    ,s.weather_main
    ,s.weather_description

    ,s.weather_icon
    ,dwi.description as eng_description

    ,s.temp
    ,s.feels_like
    ,s.temp_min
    ,s.temp_max
    ,s.pressure
    ,s.humidity
    ,s.visibility

    ,s.wind_speed
    ,s.wind_deg
    ,s.wind_gust
    ,s.clouds_all

    ,s.event_ts
    ,s.ingest_ts

    ,s.event_date
    ,s.event_hour
from stg_data s
inner join {{ source('weather_data', 'dim_city') }} as dc
    on s.city_id = dc.id
inner join {{ source('weather_data', 'dim_weather') }} as dw
    on s.weather_id = dw.id
inner join {{ source('weather_data', 'dim_weather_icon') }} as dwi
    on s.weather_icon = dwi.id
