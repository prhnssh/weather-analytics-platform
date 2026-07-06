import requests
import pandas as pd

def extract_weather():
    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": 54.71,
        "longitude": 20.51,
        "start_date": "2025-01-01",
        "end_date": "2025-01-31",
        "hourly": "temperature_2m,precipitation,wind_speed_10m"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(data["hourly"])
    df["time"] = pd.to_datetime(df["time"])

    return df


if __name__ == "__main__":
    df = extract_weather()
    print(df.head())