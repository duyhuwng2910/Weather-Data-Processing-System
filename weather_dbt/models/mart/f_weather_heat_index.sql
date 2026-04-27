{{
    config(
        materialized='table'
    )
}}


with
heat_index_calc as (
    select
         city_id
        ,event_ts
        ,event_date
        ,event_hour

        ,temp
        ,humidity

        -- Công thức Steadman, áp dụng khi temp >= 27°C và humidity >= 40%
        -- Dưới ngưỡng này heat index xấp xỉ bằng nhiệt độ thực tế
        ,(case
            when temp >= 27 and humidity >= 40
            then round(
                -8.78469475556
                + (1.61139411    * temp)
                + (2.33854883889 * humidity)
                - (0.14611605    * temp * humidity)
                - (0.012308094   * pow(temp, 2))
                - (0.0164248277778 * pow(humidity, 2))
                + (0.002211732   * pow(temp, 2) * humidity)
                + (0.00072546    * temp * pow(humidity, 2))
                - (0.000003582   * pow(temp, 2) * pow(humidity, 2))
            , 1)
            else round(temp, 1)
        end) as heat_index

        ,wind_speed

        -- Phân loại gió theo thang Beaufort
        ,(case
            when wind_speed < 0.3 then 0
            when wind_speed >= 0.3 and wind_speed < 1.6 then 1
            when wind_speed >= 1.6 and wind_speed < 3.4 then 2
            when wind_speed >= 3.4 and wind_speed < 5.5 then 3
            when wind_speed >= 5.5 and wind_speed < 8.0 then 4
            when wind_speed >= 8.0 and wind_speed < 10.8 then 5
            when wind_speed >= 10.8 and wind_speed < 13.9 then 6
            when wind_speed >= 13.9 and wind_speed < 17.2 then 7
            when wind_speed >= 17.2 and wind_speed < 20.8 then 8
            when wind_speed >= 20.8 and wind_speed < 24.5 then 9
            when wind_speed >= 24.5 and wind_speed < 28.5 then 10
            when wind_speed >= 28.5 and wind_speed < 32.7 then 11
            else 12
        end) as beaufort_scale

    from {{ ref('f_weather_hourly') }}
    where event_date = date(convert_tz(current_timestamp(), '+00:00', '+07:00'))
),
heat_index_labeled as (
    select
         city_id
        ,event_ts
        ,event_date
        ,event_hour

        ,temp
        ,humidity
        ,heat_index

        ,(case
            when heat_index < 27 then 'bình thường'
            when heat_index < 32 then 'thận trọng'
            when heat_index < 41 then 'rất khó chịu'
            else 'nguy hiểm'
        end) as heat_index_level

        ,wind_speed
        ,beaufort_scale

        ,(case
            when beaufort_scale = 0 then 'lặng gió'
            when beaufort_scale <= 2 then 'gió nhẹ'
            when beaufort_scale <= 4 then 'gió vừa'
            when beaufort_scale <= 6 then 'gió khá mạnh'
            when beaufort_scale <= 8 then 'gió mạnh'
            when beaufort_scale <= 10 then 'bão nhỏ'
            when beaufort_scale <= 11 then 'bão'
            else 'bão dữ dội'
        end) as beaufort_description

    from heat_index_calc
)
select *
from heat_index_labeled
