import pandas as pd

from backend.pipeline import clean_dataframe


def test_pipeline_fill_mean():
    dataframe = pd.DataFrame({
        "name": ["John", "Bob", "Alice"],
        "salary": [50000, None, 70000],
    })

    result, command, confidence, summary = clean_dataframe(
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

    assert summary["column"] == "salary"
    assert summary["missing_before"] == 1
    assert summary["missing_after"] == 0
    assert summary["values_filled"] == 1

    assert pd.isna(dataframe.loc[1, "salary"])


def test_pipeline_remove_duplicates():
    dataframe = pd.DataFrame({
        "name": ["John", "Bob", "John"],
        "age": [20, 25, 20],
    })

    result, command, confidence, summary = clean_dataframe(
        dataframe,
        "Get rid of duplicate records",
    )

    assert command == {
        "action": "remove_duplicates",
    }

    assert 0 <= confidence <= 1

    assert len(result) == 2
    assert len(dataframe) == 3

    assert summary["rows_before"] == 3
    assert summary["rows_after"] == 2
    assert summary["rows_removed"] == 1


def test_pipeline_remove_missing_rows():
    dataframe = pd.DataFrame({
        "name": ["John", "Bob", "Alice"],
        "age": [20, None, 30],
    })

    result, command, confidence, summary = clean_dataframe(
        dataframe,
        "Remove rows with missing values",
    )

    assert command == {
        "action": "remove_missing_rows",
    }

    assert 0 <= confidence <= 1

    assert len(result) == 2
    assert len(dataframe) == 3

    assert summary["rows_before"] == 3
    assert summary["rows_after"] == 2
    assert summary["rows_removed"] == 1


def test_pipeline_drop_column():
    dataframe = pd.DataFrame({
        "name": ["John", "Bob"],
        "age": [20, 25],
        "salary": [50000, 60000],
    })

    result, command, confidence, summary = clean_dataframe(
        dataframe,
        "Remove the salary column",
    )

    assert command == {
        "action": "drop_column",
        "column": "salary",
    }

    assert 0 <= confidence <= 1

    assert "salary" not in result.columns
    assert "salary" in dataframe.columns

    assert summary["column_removed"] == "salary"
    assert summary["columns_before"] == 3
    assert summary["columns_after"] == 2


def test_pipeline_rename_column():
    dataframe = pd.DataFrame({
        "employee_id": [1, 2, 3],
        "name": ["John", "Bob", "Alice"],
    })

    result, command, confidence, summary = clean_dataframe(
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

    assert summary["old_name"] == "employee_id"
    assert summary["new_name"] == "worker_id"

    assert "employee_id" in dataframe.columns
    assert "worker_id" not in dataframe.columns