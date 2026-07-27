import pandas as pd

from backend.pipeline import clean_dataframe


def test_pipeline_fill_mean():
    dataframe = pd.DataFrame({
        "name": ["John", "Bob", "Alice"],
        "salary": [50000, None, 70000],
    })

    result, command, confidence = clean_dataframe(
        dataframe,
        "Fill missing salary values with the average",
    )

    assert command == {
        "action": "fill_missing_with_mean",
        "column": "salary",
    }

    assert 0 <= confidence <= 1

    assert result.loc[1, "salary"] == 60000
    assert result["salary"].isna().sum() == 0

    assert pd.isna(dataframe.loc[1, "salary"])


def test_pipeline_remove_duplicates():
    dataframe = pd.DataFrame({
        "name": ["John", "Bob", "John"],
        "age": [20, 25, 20],
    })

    result, command, confidence = clean_dataframe(
        dataframe,
        "Get rid of duplicate records",
    )

    assert command == {
        "action": "remove_duplicates",
    }

    assert 0 <= confidence <= 1

    assert len(result) == 2
    assert len(dataframe) == 3


def test_pipeline_rename_column():
    dataframe = pd.DataFrame({
        "employee_id": [1, 2, 3],
        "name": ["John", "Bob", "Alice"],
    })

    result, command, confidence = clean_dataframe(
        dataframe,
        "Rename employee_id to worker_id",
    )

    assert command == {
        "action": "rename_column",
        "column": "employee_id",
        "new_name": "worker_id",
    }

    assert 0 <= confidence <= 1

    assert "worker_id" in result.columns
    assert "employee_id" not in result.columns

    assert "employee_id" in dataframe.columns