import pandas as pd

from backend.csv_analyzer import analyze_dataframe


def test_analyze_dataframe():
    dataframe = pd.DataFrame({
        "name": ["John", "Bob", "John"],
        "age": [20, None, 20],
        "salary": [50000, 60000, 50000]
    })

    result = analyze_dataframe(dataframe)

    assert result["row_count"] == 3
    assert result["column_count"] == 3
    assert result["columns"] == [
        "name",
        "age",
        "salary"
    ]

    assert result["missing_values"]["age"] == 1
    assert result["duplicate_rows"] == 1

    assert "age" in result["numeric_columns"]
    assert "salary" in result["numeric_columns"]
    assert "name" not in result["numeric_columns"]