import pandas as pd

from backend.actions import remove_duplicates


def test_remove_duplicates():
    dataframe = pd.DataFrame({
        "name": ["John", "Bob", "John"],
        "age": [20, 25, 20]
    })

    result = remove_duplicates(dataframe)

    assert len(result) == 2