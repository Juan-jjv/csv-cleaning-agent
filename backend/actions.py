import pandas as pd

def remove_duplicates(dataframe: pd.DataFrame) -> pd.DataFrame:
    cleaned_dataframe = dataframe.drop_duplicates()
    cleaned_dataframe = cleaned_dataframe.reset_index(drop=True)

    return cleaned_dataframe

def remove_missing_rows(dataframe: pd.DataFrame) -> pd.DataFrame:
    cleaned_dataframe = dataframe.dropna()
    cleaned_dataframe = cleaned_dataframe.reset_index(drop=True)

    return cleaned_dataframe