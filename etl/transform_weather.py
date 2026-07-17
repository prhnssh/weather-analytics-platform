import os
import pandas as pd


def transform_weather(input_path, output_path):
    """
    Преобразовываем необработанные данные о погоде
    в агрегированный набор данных за день.
    """

    # читаем все CSV из raw слоя
    files = [
        f for f in os.listdir(input_path)
        if f.endswith(".csv")
    ]

    all_data = []

    for file in files:

        df = pd.read_csv(
            os.path.join(input_path, file)
        )

        # приводим время к datetime
        df["time"] = pd.to_datetime(df["time"])

        # создаем отдельную колонку даты без времени 
        df["date"] = df["time"].dt.normalize()


        # агрегируем до дня
        daily = df.groupby(
            ["city", "date"]
        ).agg(
            avg_temp=("temperature_2m", "mean"),
            max_temp=("temperature_2m", "max"),
            min_temp=("temperature_2m", "min"),
            total_precip=("precipitation", "sum"),
            avg_wind=("wind_speed_10m", "mean")
        ).reset_index()


        all_data.append(daily)


    # объединяем города
    result = pd.concat(
        all_data,
        ignore_index=True
    )


    # проверяем типы
    print(result.dtypes)


    # создаем processed слой
    os.makedirs(
        output_path,
        exist_ok=True
    )


    output_file = os.path.join(
        output_path,
        "weather_daily.csv"
    )


    result.to_csv(
        output_file,
        index=False
    )


    print(
        f"Преобразование завершено. Файл сохранен: {output_file}"
    )


    return result



if __name__ == "__main__":

    df = transform_weather(
        input_path="data/raw",
        output_path="data/processed"
    )

    print(df.head())