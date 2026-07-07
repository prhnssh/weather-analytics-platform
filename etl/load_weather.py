import pandas as pd
from sqlalchemy import create_engine


# подключение к PostgreSQL
engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/analytics"
)


# загрузка обработанных данных
df = pd.read_csv("data/processed/weather_daily.csv")


# загрузка данных в PostgreSQL
df.to_sql(
    "weather_daily",
    engine,
    schema="weather",
    if_exists="append",
    index=False
)


print("Данные успешно загружены")