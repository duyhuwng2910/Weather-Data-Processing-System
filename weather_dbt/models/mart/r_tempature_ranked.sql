select
     w.event_date
    ,c.id as city_id
    ,c.name as city_name
    ,w.avg_temp

from {{ source('weather_data', 'dim_city') }} c
inner join {{ ref('f_weather_daily') }} w
    on c.id = w.city_id
where
    w.event_date = current_date
order by w.avg_temp desc
