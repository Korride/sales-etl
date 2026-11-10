import logging

import pandas as pd

from config import raw_data_path

logger = logging.getLogger(__name__)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)

    df = df.copy()
    df = df.drop_duplicates()
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["country"] = df["country"].str.strip().str.title()
    df["category"] = df["category"].fillna("Unknown")
    df = df.dropna(subset=["unit_price"])
    df["revenue"] = df["quantity"] * df["unit_price"]

    after = len(df)
    logger.info(
        "Transform: rows before %d, rows after %d (dropped %d)",
        before, after, before - after,
    )
    return df


def build_marts(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    by_category = (
        df.groupby("category", as_index=False)
        .agg(orders=("order_id", "count"), revenue=("revenue", "sum"))
        .sort_values(by="revenue", ascending=False)
    )

    by_country = (
        df.groupby("country", as_index=False)
        .agg(orders=("order_id", "count"), revenue=("revenue", "sum"))
        .sort_values(by="revenue", ascending=False)
    )

    by_month = (
        df.assign(month=df["order_date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)
        .agg(orders=("order_id", "count"), revenue=("revenue", "sum"))
        .sort_values("month")
    )

    return {
        "revenue_by_category": by_category,
        "revenue_by_country": by_country,
        "revenue_by_month": by_month,
    }


if __name__ == "__main__":
    from logging_config import setup_logging

    setup_logging()
    clean = transform(pd.read_csv(raw_data_path))
    for name, table in build_marts(clean).items():
        logger.info("\n=== %s ===\n%s", name, table)