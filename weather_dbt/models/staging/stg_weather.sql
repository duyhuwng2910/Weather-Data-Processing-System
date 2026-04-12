with
source as (
    select *
    from {{ source('weather_data', 'weather_raw') }}
    where ingest_ts = date_format(current_timestamp(), '%Y-%m-%d %H:00:00')
),
cleaned as (
    select
         city_id

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

        ,event_ts
        ,ingest_ts

        ,date(event_ts) as event_date
        ,hour(event_ts) as event_hour
    from source
)
select *
from cleaned
