import pandas as pd
from sqlalchemy import create_engine


def load_daily_weather(input_path):
    """
    Загружаем обработанные данные о погоде в PostgreSQL.
    """

    engine = create_engine(
        "postgresql://airflow:airflow@postgres:5432/airflow"
    )

    df = pd.read_csv(input_path)

    df.to_sql(
        "weather_daily",
        engine,
        schema="weather",
        if_exists="append",
        index=False
    )

    print("Данные успешно загружены в PostgreSQL")

    return True