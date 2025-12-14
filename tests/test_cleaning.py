import pytest
import pandas as pd
import numpy as np
from utah_housing_stat386.cleaning import (
    clean_price, clean_numeric_field, clean_year_built,
    clean_lot_size, clean_garage, clean_housing_data
)


def test_clean_price():
    assert clean_price("$481,999") == 481999.0
    assert clean_price("$1,234,567") == 1234567.0
    assert pd.isna(clean_price(""))
    assert pd.isna(clean_price(None))


def test_clean_numeric_field():
    assert clean_numeric_field("1,252") == 1252.0
    assert clean_numeric_field("3") == 3.0
    assert pd.isna(clean_numeric_field(""))


def test_clean_year_built():
    assert clean_year_built("1919") == 1919
    assert clean_year_built("2024") == 2024
    assert pd.isna(clean_year_built("1799"))  # Too old
    assert pd.isna(clean_year_built(""))


def test_clean_lot_size():
    assert clean_lot_size("0.10 Ac") == 0.10
    assert abs(clean_lot_size("4356 sq ft") - 0.1) < 0.01
    assert pd.isna(clean_lot_size(""))


def test_clean_garage():
    assert clean_garage("2") == 2
    assert clean_garage("") == 0


def test_clean_housing_data():
    df = pd.DataFrame({
        'price': ['$100,000', '$200,000'],
        'beds': ['3', '4'],
        'baths': ['2', '3']
    })

    df_clean = clean_housing_data(df)

    assert df_clean['price'].iloc[0] == 100000.0
    assert df_clean['beds'].iloc[0] == 3.0
