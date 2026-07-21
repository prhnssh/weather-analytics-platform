import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook
from sqlalchemy.types import Date


def load_daily_weather(input_path):
    """
    Загружаем обработанные данные о погоде в PostgreSQL.
    """

    hook = PostgresHook(
        postgres_conn_id="postgres_analitica"
    )

    engine = hook.get_sqlalchemy_engine()

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