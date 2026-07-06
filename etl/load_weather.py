import pandas as pd
from sqlalchemy import create_engine


def load_weather(file_path):
    """
    Load transformed weather data into PostgreSQL
    """

    df = pd.read_csv(file_path)

    # подключение к БД 
    engine = create_engine("postgresql://user:password@localhost:5432/weather_db")

    df.to_sql(
        "weather_daily",
        engine,
        if_exists="replace",
        index=False
    )

    print("Data loaded into PostgreSQL")


if __name__ == "__main__":
    load_weather("data/processed/weather_daily.csv")
