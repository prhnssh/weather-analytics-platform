import pandas as pd
from sqlalchemy import create_engine


# подключение к PostgreSQL
engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/analytics"
)


# читаем подготовленные данные
df = pd.read_csv("../data/processed/weather.csv")


# загружаем в PostgreSQL
df.to_sql(
    "weather_data",
    engine,
    schema="weather",
    if_exists="append",
    index=False
)


print("Данные успешно загружены")
