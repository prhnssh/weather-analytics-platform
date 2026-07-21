import pandas as pd
import glob
from airflow.providers.postgres.hooks.postgres import PostgresHook


def load_raw_weather(input_path):
    """
    Загружаем сырые данные о погоде в PostgreSQL.
    """

    hook = PostgresHook(
        postgres_conn_id="postgres_analitica"
    )

    engine = hook.get_sqlalchemy_engine()

    files = glob.glob(f"{input_path}/*.csv")

    all_data = []

    for file in files:
        df = pd.read_csv(file)

        city = file.split("weather_raw_")[1].split("_2025")[0]

        df["city"] = city

        all_data.append(df)

    result = pd.concat(all_data, ignore_index=True)

    result.to_sql(
        "weather_raw",
        engine,
        schema="weather",
        if_exists="append",
        index=False
    )

    print("Исходные данные загружены:", len(result))