
DROP TABLE IF EXISTS mart.weather_monthly_dashboard;


CREATE TABLE mart.weather_monthly_dashboard AS

SELECT
    city,
    DATE_TRUNC('month', date::date)::date AS month,
    EXTRACT(MONTH FROM date)::int AS month_number,

    CASE
        WHEN EXTRACT(MONTH FROM date) = 1 THEN 'Январь'
        WHEN EXTRACT(MONTH FROM date) = 2 THEN 'Февраль'
        WHEN EXTRACT(MONTH FROM date) = 3 THEN 'Март'
        WHEN EXTRACT(MONTH FROM date) = 4 THEN 'Апрель'
        WHEN EXTRACT(MONTH FROM date) = 5 THEN 'Май'
        WHEN EXTRACT(MONTH FROM date) = 6 THEN 'Июнь'
        WHEN EXTRACT(MONTH FROM date) = 7 THEN 'Июль'
        WHEN EXTRACT(MONTH FROM date) = 8 THEN 'Август'
        WHEN EXTRACT(MONTH FROM date) = 9 THEN 'Сентябрь'
        WHEN EXTRACT(MONTH FROM date) = 10 THEN 'Октябрь'
        WHEN EXTRACT(MONTH FROM date) = 11 THEN 'Ноябрь'
        WHEN EXTRACT(MONTH FROM date) = 12 THEN 'Декабрь'
    END AS month_name,

    ROUND(AVG(avg_temp)::numeric, 2) AS avg_temp,
    ROUND(MAX(max_temp)::numeric, 2) AS max_temp,
    ROUND(MIN(min_temp)::numeric, 2) AS min_temp,

    ROUND(SUM(total_precip)::numeric, 2) AS total_precip,
    ROUND(AVG(avg_wind)::numeric, 2) AS avg_wind

FROM weather.weather_daily

GROUP BY
    city,
    DATE_TRUNC('month', date::date)::date,
    EXTRACT(MONTH FROM date);

