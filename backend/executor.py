import pandas as pd

from backend.actions import (
    remove_duplicates,
    remove_missing_rows,
    fill_missing_with_median,
    fill_missing_with_mean,
    drop_column,
    rename_column,
)

def execute_action(
    dataframe: pd.DataFrame,
    command: dict
) -> pd.DataFrame:

    action = command.get("action")

    if action == "remove_duplicates":
        return remove_duplicates(dataframe)

    elif action == "remove_missing_rows":
        return remove_missing_rows(dataframe)

    elif action == "fill_missing_with_median":
        return fill_missing_with_median(
            dataframe,
            command["column"]
        )

    elif action == "fill_missing_with_mean":
        return fill_missing_with_mean(
            dataframe,
            command["column"]
        )

    elif action == "drop_column":
        return drop_column(
            dataframe,
            command["column"]
        )

    elif action == "rename_column":
        return rename_column(
            dataframe,
            command["column"],
            command["new_name"]
        )

    else:
        raise ValueError(f"Unsupported action: {action}")