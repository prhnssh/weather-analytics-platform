import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import Date


def load_daily_weather(input_path):
    """
    Загружаем обработанные данные о погоде в PostgreSQL.
    """

    engine = create_engine(
        "postgresql://airflow:airflow@postgres:5432/airflow"
    )

    df = pd.read_csv(input_path)

    df["date"] = pd.to_datetime(df["date"])

    df.to_sql(
        "weather_daily",
        engine,
        schema="weather",
        if_exists="replace",
        index=False,
        dtype={
            "date": Date()
        }
    )

    print("Данные успешно загружены в PostgreSQL")

    return True


if __name__ == "__main__":

    load_daily_weather(
        input_path="data/processed/weather_daily.csv"
    )