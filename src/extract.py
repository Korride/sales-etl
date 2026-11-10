import logging

import pandas as pd

from config import raw_data_path

logger = logging.getLogger(__name__)


def extract(path: str = raw_data_path) -> pd.DataFrame:
    logger.info("Extract: reading %s", path)
    df = pd.read_csv(path)
    logger.info("Extract: loaded %d rows, %d columns", len(df), df.shape[1])
    logger.debug("Extract: preview\n%s", df.head())
    return df


if __name__ == "__main__":
    from logging_config import setup_logging

    setup_logging()
    extract()("data/raw/sales.csv")