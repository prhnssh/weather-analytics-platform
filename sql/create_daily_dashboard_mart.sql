CREATE SCHEMA IF NOT EXISTS mart;


DROP TABLE IF EXISTS mart.weather_daily_dashboard;


CREATE TABLE mart.weather_daily_dashboard AS

SELECT
    city,
    date::date AS date,

    avg_temp,
    max_temp,
    min_temp,
    total_precip,
    avg_wind,

    CASE
        WHEN EXTRACT(MONTH FROM date::date) IN (12,1,2)
            THEN 'Зима'
        WHEN EXTRACT(MONTH FROM date::date) IN (3,4,5)
            THEN 'Весна'
        WHEN EXTRACT(MONTH FROM date::date) IN (6,7,8)
            THEN 'Лето'
        ELSE 'Осень'
    END AS season,

    CASE
        WHEN avg_temp < 0 THEN 'Холодно'
        WHEN avg_temp BETWEEN 0 AND 15 THEN 'Прохладно'
        ELSE 'Тепло'
    END AS temp_category

FROM weather.weather_daily;


