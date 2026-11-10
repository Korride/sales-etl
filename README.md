# Sales ETL

Учебный ETL-пайплайн: сырые продажи из CSV → очистка и агрегация на pandas →
загрузка в PostgreSQL.

## Архитектура

    CSV (raw)  ──►  Extract  ──►  Transform  ──►  Load  ──►  PostgreSQL
    data/raw/      pandas        чистка +        to_sql      БД sales_dw,
    sales.csv      DataFrame     витрины         (SQLAlchemy) схема sales

## Требования

- Python 3.11+
- PostgreSQL (в проекте используется контейнер Docker на порту 5434)

## Установка

    python -m venv .venv
    .venv\Scripts\Activate.ps1        # Windows PowerShell
    pip install -r requirements.txt

Создать базу данных (если ещё нет):

    CREATE DATABASE sales_dw;

## Запуск

    python src/generate_data.py       # сгенерировать сырой CSV (детерминированно)
    python src/pipeline.py            # прогнать весь ETL

## Тесты

    python -m pytest -v

## Структура

    src/
      config.py          # настройки и строка подключения к БД
      generate_data.py   # генератор грязных данных
      extract.py         # E: чтение CSV
      transform.py       # T: очистка и витрины
      load.py            # L: загрузка в PostgreSQL
      pipeline.py        # оркестратор
      logging_config.py  # настройка логирования
    tests/
      test_transform.py  # проверки качества данных