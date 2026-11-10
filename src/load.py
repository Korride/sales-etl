import logging

import pandas as pd
from sqlalchemy import create_engine, text

from config import DB_URL, SCHEMA, raw_data_path

logger = logging.getLogger(__name__)


def ensure_schema(engine) -> None:
    with engine.begin() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA};"))


def load(df: pd.DataFrame, table_name: str, engine) -> None:
    df.to_sql(
        table_name,
        engine,
        schema=SCHEMA,
        if_exists="replace",
        index=False,
    )
    with engine.connect() as conn:
        cnt = conn.execute(
            text(f"SELECT COUNT(*) FROM {SCHEMA}.{table_name};")
        ).scalar()
    logger.info("Load: %s.%s -> %d rows", SCHEMA, table_name, cnt)


def main() -> None:
    from transform import build_marts, transform

    engine = create_engine(DB_URL)
    ensure_schema(engine)

    raw = pd.read_csv(raw_data_path)
    clean = transform(raw)

    load(clean, "stg_sales", engine)
    for name, table in build_marts(clean).items():
        load(table, name, engine)


if __name__ == "__main__":
    from logging_config import setup_logging

    setup_logging()
    main()