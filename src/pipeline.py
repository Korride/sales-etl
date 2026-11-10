import logging
import time

from sqlalchemy import create_engine

from config import DB_URL, raw_data_path
from extract import extract
from load import ensure_schema, load
from logging_config import setup_logging
from transform import build_marts, transform

logger = logging.getLogger(__name__)


def run_pipeline() -> None:
    started = time.perf_counter()
    logger.info("Pipeline started")

    engine = create_engine(DB_URL)
    ensure_schema(engine)

    raw = extract(raw_data_path)
    clean = transform(raw)

    load(clean, "stg_sales", engine)
    for name, table in build_marts(clean).items():
        load(table, name, engine)

    elapsed = time.perf_counter() - started
    logger.info("Pipeline finished in %.2f seconds", elapsed)


if __name__ == "__main__":
    setup_logging()
    run_pipeline()