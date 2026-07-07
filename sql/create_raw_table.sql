CREATE TABLE IF NOT EXISTS weather.weather_raw (
    time TIMESTAMP,
    temperature_2m FLOAT,
    precipitation FLOAT,
    wind_speed_10m FLOAT,
    city TEXT,
    load_date TIMESTAMP,
    latitude FLOAT,
    longitude FLOAT
);