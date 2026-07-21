from etl.extract_weather import extract_weather
from etl.load_raw_weather import load_raw_weather
from etl.transform_weather import transform_weather
from etl.load_daily_weather import load_daily_weather
from etl.build_dashboard_mart import build_dashboard_mart
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


START_DATE = datetime(2026, 7, 8)


default_args = {
    "owner": "analytics",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="weather_etl",
    default_args=default_args,
    start_date=START_DATE,
    schedule="@daily",
    catchup=False,
) as dag:

    cities = [
        {
            "city_name": "Kaliningrad",
            "latitude": 54.71,
            "longitude": 20.51,
        },
        {
            "city_name": "Moscow",
            "latitude": 55.75,
            "longitude": 37.61,
        },
        {
            "city_name": "Saint_Petersburg",
            "latitude": 59.93,
            "longitude": 30.31,
        },
    ]

    extract_tasks = []

    for city in cities:

        task = PythonOperator(
            task_id=f"extract_{city['city_name'].lower()}",
            python_callable=extract_weather,
            op_kwargs={
                "latitude": city["latitude"],
                "longitude": city["longitude"],
                "city_name": city["city_name"],
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "output_path": "/opt/airflow/data/raw",
            },
        )

        extract_tasks.append(task)

    raw_task = PythonOperator(
        task_id="load_raw_weather",
        python_callable=load_raw_weather,
        op_kwargs={
            "input_path": "/opt/airflow/data/raw",
    },
)

    transform_task = PythonOperator(
        task_id="transform_weather",
        python_callable=transform_weather,
        op_kwargs={
            "input_path": "/opt/airflow/project/data/raw",
            "output_path": "/opt/airflow/project/data/processed",
    },
)

    load_task = PythonOperator(
         task_id="load_daily_weather",
         python_callable=load_daily_weather,
         op_kwargs={
             "input_path": "/opt/airflow/project/data/processed/weather_daily.csv",
    },
)

    build_mart_task = PythonOperator(
        task_id="build_dashboard_mart",
        python_callable=build_dashboard_mart
)

    for task in extract_tasks:
        task >> raw_task

    raw_task >> transform_task >> load_task >> build_mart_task