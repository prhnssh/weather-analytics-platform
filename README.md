# Weather Analytics Platform

ETL-проект по сбору, обработке и анализу погодных данных.

## Описание проекта

Проект реализует полный ETL-процесс:

- получение погодных данных через API;
- сохранение исходных почасовых данных;
- обработку и агрегацию данных;
- загрузку данных в PostgreSQL;
- подготовку данных для аналитики.

В качестве источника данных используется Open-Meteo API.

Данные собираются для городов:

- Moscow
- Saint Petersburg
- Kaliningrad

Период анализа: 2025 год.

---

## Архитектура проекта


Open-Meteo API
|
↓
extract_weather.py
|
↓
data/raw
(почасовые данные)
|
├───────────────┐
↓ ↓
load_raw_weather.py transform_weather.py
↓ ↓
PostgreSQL data/processed
weather.weather_raw |
↓
load_daily_weather.py
|
↓
PostgreSQL
weather.weather_daily


---

## Структура проекта


weather-analytics-platform/

├── data/
│ ├── raw/
│ │ └── почасовые данные из API
│ │
│ └── processed/
│ └── агрегированные данные по дням
│
├── etl/
│ ├── extract_weather.py
│ ├── load_raw_weather.py
│ ├── transform_weather.py
│ └── load_daily_weather.py
│
├── sql/
│ ├── create_schema.sql
│ ├── create_raw_table.sql
│ └── create_daily_table.sql
│
├── notebooks/
│ └── анализ данных
│
└── README.md


---

## ETL-процесс

### 1. Extract

Скрипт:


etl/extract_weather.py


Получает данные через API и сохраняет почасовые данные в:


data/raw/


Основные параметры:

- температура воздуха (`temperature_2m`);
- осадки (`precipitation`);
- скорость ветра (`wind_speed_10m`);
- время измерения.

---

### 2. Load Raw

Скрипт:


etl/load_raw_weather.py


Загружает исходные данные без изменений в таблицу:


weather.weather_raw


Raw слой используется как источник для дальнейшей обработки.

---

### 3. Transform

Скрипт:


etl/transform_weather.py


Преобразует почасовые данные в дневные показатели:

- средняя температура;
- максимальная температура;
- минимальная температура;
- количество осадков за день;
- средняя скорость ветра.

Результат сохраняется:


data/processed/weather_daily.csv


---

### 4. Load Daily

Скрипт:


etl/load_daily_weather.py


Загружает обработанные данные в таблицу:


weather.weather_daily


---

## Используемые технологии

- Python
- Pandas
- Requests
- PostgreSQL
- SQLAlchemy
- Docker
- Git

---

## База данных

Используется PostgreSQL.

Схема:


weather


Таблицы:

### weather_raw

Содержит исходные почасовые данные:

- time
- city
- temperature_2m
- precipitation
- wind_speed_10m
- latitude
- longitude
- load_date


### weather_daily

Содержит агрегированные данные:

- city
- date
- avg_temp
- max_temp
- min_temp
- total_precip
- avg_wind

---

## Запуск проекта

1. Установить зависимости:


pip install -r requirements.txt


2. Получить данные:


python etl/extract_weather.py


3. Загрузить raw слой:


python etl/load_raw_weather.py


4. Выполнить обработку:


python etl/transform_weather.py


5. Загрузить дневную витрину:


python etl/load_daily_weather.py


---

## Цель проекта

Проект демонстрирует навыки:

- построения ETL pipeline;
- работы с REST API;
- обработки данных в Python;
- работы с PostgreSQL;
- проектирования слоев хранения данных;
- подготовки данных для аналитики.