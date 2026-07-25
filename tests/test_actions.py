import pandas as pd

from backend.actions import remove_duplicates, remove_missing_rows

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