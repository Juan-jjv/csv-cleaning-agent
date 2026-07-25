import pandas as pd

def remove_duplicates(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe.drop_duplicates().reset_index(drop=True)

def remove_missing_rows(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe.dropna().reset_index(drop=True)

def fill_missing_with_median(
    dataframe: pd.DataFrame,
    column: str
) -> pd.DataFrame:

    if not pd.api.types.is_numeric_dtype(dataframe[column]):
        raise ValueError(f"Column '{column}' must be numeric.")

    median = dataframe[column].median()

    dataframe[column] = dataframe[column].fillna(median)

    return dataframe

def fill_missing_with_mean(
    dataframe: pd.DataFrame,
    column: str
) -> pd.DataFrame:

    if not pd.api.types.is_numeric_dtype(dataframe[column]):
        raise ValueError(f"Column '{column}' must be numeric.")

    mean = dataframe[column].mean()

    dataframe[column] = dataframe[column].fillna(mean)

    return dataframe

def drop_column(
    dataframe: pd.DataFrame,
    column: str
) -> pd.DataFrame:

    if column not in dataframe.columns:
        raise ValueError(f"Column '{column}' does not exist.")

    return dataframe.drop(columns=[column])

def rename_column(
    dataframe: pd.DataFrame,
    column: str,
    new_name: str
) -> pd.DataFrame:

    if column not in dataframe.columns:
        raise ValueError(f"Column '{column}' does not exist.")

    if new_name in dataframe.columns and new_name != column:
        raise ValueError(f"Column '{new_name}' already exists.")

    return dataframe.rename(columns={column: new_name})