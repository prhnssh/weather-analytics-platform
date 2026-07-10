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

    pass