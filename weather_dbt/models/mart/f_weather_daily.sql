select
     city_id
    ,event_date

    ,avg(temp) as avg_temp
    ,min(temp) as min_temp
    ,max(temp) as max_temp

    ,avg(humidity) as avg_humidity
    ,avg(wind_speed) as avg_wind_speed
from {{ ref('stg_weather') }}
group by city_id, event_date
