import requests
import pandas as pd
from datetime import datetime
import os


def extract_weather(latitude, longitude, city_name, start_date, end_date, output_path):
    """
    Получаем данные о погоде для конкретного города из Open-Meteo API и сохраняем исходный набор данных локально.
    """

    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m,precipitation,wind_speed_10m"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(data["hourly"])
    df["time"] = pd.to_datetime(df["time"])

    # добавляем метаданные
    df["city"] = city_name
    df["load_date"] = datetime.now()
    df["latitude"] = latitude
    df["longitude"] = longitude

    # создаём папку
    os.makedirs(output_path, exist_ok=True)

    file_name = f"weather_raw_{city_name}_{start_date}_{end_date}.csv"
    full_path = os.path.join(output_path, file_name)

    df.to_csv(full_path, index=False)

    print(f"Data saved to: {full_path}")

    return df


if __name__ == "__main__":

    cities = [
        {"name": "Kaliningrad", "lat": 54.71, "lon": 20.51},
        {"name": "Moscow", "lat": 55.75, "lon": 37.61},
        {"name": "Saint_Petersburg", "lat": 59.93, "lon": 30.31}
    ]

    all_data = []

    for city in cities:
        df = extract_weather(
            latitude=city["lat"],
            longitude=city["lon"],
            city_name=city["name"],
            start_date="2025-01-01",
            end_date="2025-01-31",
            output_path="data/raw"
        )

        all_data.append(df)

    final_df = pd.concat(all_data, ignore_index=True)

    print(final_df.head())