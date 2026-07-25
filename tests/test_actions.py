import pandas as pd

from backend.actions import (
    remove_duplicates,
    remove_missing_rows,
    fill_missing_with_median,
    fill_missing_with_mean,
)

def test_remove_duplicates():
    dataframe = pd.DataFrame({
        "name": ["John", "Bob", "John"],
        "age": [20, 25, 20]
    })

    result = remove_duplicates(dataframe)

    assert len(result) == 2
    assert list(result["name"]) == ["John", "Bob"]
    assert list(result["age"]) == [20, 25]

def test_remove_missing_rows():
    dataframe = pd.DataFrame({
        "name": ["John", "Bob", "Alice"],
        "age": [20, None, 25]
    })

    result = remove_missing_rows(dataframe)

    assert len(result) == 2
    assert result.loc[0, "name"] == "John"
    assert result.loc[1, "name"] == "Alice"

def test_fill_missing_with_median():
    dataframe = pd.DataFrame({
        "age": [20, None, 40]
    })

    result = fill_missing_with_median(dataframe, "age")

    assert result.loc[1, "age"] == 30
    assert result["age"].isna().sum() == 0

def test_fill_missing_with_mean():
    dataframe = pd.DataFrame({
        "age": [10, 20, None, 30]
    })

    result = fill_missing_with_mean(dataframe, "age")

    assert result.loc[2, "age"] == 20
    assert result["age"].isna().sum() == 0