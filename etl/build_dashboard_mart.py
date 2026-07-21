from pathlib import Path

from airflow.providers.postgres.hooks.postgres import PostgresHook


def build_dashboard_mart():
    """
    Создание витрин для дашборда погоды.
    """

    hook = PostgresHook(
        postgres_conn_id="postgres_analitica"
    )

    conn = hook.get_conn()
    cursor = conn.cursor()

    sql_path = Path("/opt/airflow/project/sql")

    sql_files = [
        "create_monthly_dashboard_mart.sql",
        "create_daily_dashboard_mart.sql"
    ]

    for file_name in sql_files:
        with open(sql_path / file_name, "r") as file:
            sql = file.read()

        cursor.execute(sql)

    conn.commit()

    cursor.close()
    conn.close()

    print("Витрины для дашборда успешно созданы")

    return True