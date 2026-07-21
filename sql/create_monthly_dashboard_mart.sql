CREATE SCHEMA IF NOT EXISTS mart;


DROP TABLE IF EXISTS mart.weather_monthly_dashboard;


CREATE TABLE mart.weather_monthly_dashboard AS

SELECT
    city,
    DATE_TRUNC('month', date::date)::date AS month,

    ROUND(AVG(avg_temp)::numeric, 2) AS avg_temp,
    ROUND(MAX(max_temp)::numeric, 2) AS max_temp,
    ROUND(MIN(min_temp)::numeric, 2) AS min_temp,

    ROUND(SUM(total_precip)::numeric, 2) AS total_precip,
    ROUND(AVG(avg_wind)::numeric, 2) AS avg_wind

FROM weather.weather_daily

GROUP BY
    city,
    DATE_TRUNC('month', date::date)::date;

