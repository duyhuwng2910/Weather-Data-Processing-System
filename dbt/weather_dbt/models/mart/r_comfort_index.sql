select
     city_id
    ,event_ts
    ,temp
    ,humidity

    ,temp - (0.55 - 0.0055 * humidity) * (temp - 14.5) as comfort_index

from {{ ref('stg_weather') }}
