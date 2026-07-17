import pandas as pd
import glob
from sqlalchemy import create_engine


def load_raw_weather(input_path):

    engine = create_engine(
        "postgresql://airflow:airflow@postgres:5432/airflow"
    )

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