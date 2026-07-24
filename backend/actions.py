import pandas as pd


def remove_duplicates(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Return a new DataFrame with duplicate rows removed.
    """
    cleaned_dataframe = dataframe.drop_duplicates()
    cleaned_dataframe = cleaned_dataframe.reset_index(drop=True)

    return cleaned_dataframe