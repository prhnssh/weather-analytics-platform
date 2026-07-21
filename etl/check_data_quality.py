from airflow.providers.postgres.hooks.postgres import PostgresHook


def check_data_quality():
    """
    Проверка качества данных перед построением витрин.
    """

    hook = PostgresHook(postgres_conn_id="postgres_analitica")

    conn = hook.get_conn()
    cursor = conn.cursor()

    checks = [
        (
            "Таблица weather_daily не должна быть пустой",
            """
            SELECT COUNT(*)
            FROM weather.weather_daily;
            """,
            lambda x: x > 0
        ),
        (
            "Должно быть загружено 3 города",
            """
            SELECT COUNT(DISTINCT city)
            FROM weather.weather_daily;
            """,
            lambda x: x == 3
        ),
        (
            "Для каждого города должно быть 365 записей",
            """
            SELECT COUNT(*)
            FROM (
                SELECT city
                FROM weather.weather_daily
                GROUP BY city
                HAVING COUNT(*) <> 365
            ) t;
            """,
            lambda x: x == 0
        ),
        (
            "Не должно быть пропущенных значений",
            """
            SELECT COUNT(*)
            FROM weather.weather_daily
            WHERE
                date IS NULL
                OR avg_temp IS NULL
                OR max_temp IS NULL
                OR min_temp IS NULL;
            """,
            lambda x: x == 0
        ),
        (
            "Температуры должны удовлетворять условию min ≤ avg ≤ max",
            """
            SELECT COUNT(*)
            FROM weather.weather_daily
            WHERE
                min_temp > avg_temp
                OR avg_temp > max_temp;
            """,
            lambda x: x == 0
        )
    ]

    for description, sql, validator in checks:

        cursor.execute(sql)

        result = cursor.fetchone()[0]

        if not validator(result):
            raise ValueError(
                f"Проверка не пройдена: {description}. Результат: {result}"
            )

        print(f"✓ {description}")

    cursor.close()
    conn.close()

    print("Все проверки качества данных успешно пройдены.")

    return True