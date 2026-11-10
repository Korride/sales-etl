import pandas as pd
import pytest

from transform import transform


@pytest.fixture
def raw_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "order_id": [1, 2, 2, 3, 4],
            "order_date": [
                "2024-01-01", "2024-01-15", "2024-01-15", "2024-02-01", "2024-03-01",
            ],
            "customer": ["a", "b", "b", "c", "d"],
            "country": ["germany", "FRANCE", "FRANCE", "sPain", "  Italy "],
            "category": ["Food", None, None, "Clothing", "Food"],
            "product": ["X", "Y", "Y", "Z", "X"],
            "quantity": [1, 2, 2, 3, 4],
            "unit_price": [10.0, 20.0, 20.0, None, 5.0],
        }
    )


@pytest.fixture
def clean_df(raw_df) -> pd.DataFrame:
    result = transform(raw_df)
    assert not result.empty, "transform returned empty dataframe"
    return result


def test_row_count_after_cleaning(clean_df):
    assert len(clean_df) == 3


def test_removes_duplicates(clean_df):
    assert clean_df.duplicated().sum() == 0


def test_drops_rows_without_price(clean_df):
    assert clean_df["unit_price"].isna().sum() == 0


def test_countries_are_normalized(clean_df):
    allowed = {"Germany", "France", "Spain", "Italy", "Poland"}
    countries = set(clean_df["country"])
    assert countries, "стран нет вовсе"          # защита от пустого множества
    assert countries <= allowed


def test_no_missing_category(clean_df):
    assert clean_df["category"].isna().sum() == 0


def test_order_date_is_datetime(clean_df):
    assert pd.api.types.is_datetime64_any_dtype(clean_df["order_date"])


def test_revenue_is_computed(clean_df):
    expected = clean_df["quantity"] * clean_df["unit_price"]
    assert (clean_df["revenue"] == expected).all()


def test_data_quality_business_rules(clean_df):
    assert len(clean_df) > 0
    assert (clean_df["quantity"] > 0).all()
    assert (clean_df["unit_price"] > 0).all()
    assert (clean_df["revenue"] >= 0).all()
