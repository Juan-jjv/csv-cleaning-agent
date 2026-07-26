import pandas as pd

def analyze_dataframe(dataframe: pd.DataFrame) -> dict:
    return {
        "row_count": len(dataframe),
        "column_count": len(dataframe.columns),
        "columns": dataframe.columns.tolist(),
        "data_types": dataframe.dtypes.astype(str).to_dict(),
        "missing_values": dataframe.isna().sum().astype(int).to_dict(),
        "duplicate_rows": int(dataframe.duplicated().sum()),
        "numeric_columns": dataframe.select_dtypes(
            include="number"
        ).columns.tolist(),
    }