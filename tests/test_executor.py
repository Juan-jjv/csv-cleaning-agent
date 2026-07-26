import pandas as pd
import pytest

from backend.executor import execute_action


def test_execute_remove_duplicates():
    dataframe = pd.DataFrame({
        "name": ["John", "Bob", "John"],
        "age": [20, 25, 20]
    })

    command = {
        "action": "remove_duplicates"
    }

    result = execute_action(dataframe, command)

    assert len(result) == 2
    assert list(result["name"]) == ["John", "Bob"]

def test_execute_fill_missing_with_median():
    dataframe = pd.DataFrame({
        "age": [20, None, 40]
    })

    command = {
        "action": "fill_missing_with_median",
        "column": "age"
    }

    result = execute_action(dataframe, command)

    assert result.loc[1, "age"] == 30
    assert result["age"].isna().sum() == 0

def test_execute_invalid_action():
    dataframe = pd.DataFrame({
        "age": [20, 30, 40]
    })

    command = {
        "action": "something_invalid"
    }

    with pytest.raises(ValueError):
        execute_action(dataframe, command)