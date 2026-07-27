import pandas as pd

from backend.csv_analyzer import analyze_dataframe
from backend.executor import execute_action
from backend.validator import validate_command
from model.interpreter import interpret_instruction


def build_change_summary(
    before: dict,
    after: dict,
    command: dict,
) -> dict:

    action = command["action"]

    summary = {
        "rows_before": before["row_count"],
        "rows_after": after["row_count"],
        "columns_before": before["column_count"],
        "columns_after": after["column_count"],
    }

    if action == "remove_duplicates":
        summary["rows_removed"] = (
            before["row_count"] - after["row_count"]
        )

    elif action == "remove_missing_rows":
        summary["rows_removed"] = (
            before["row_count"] - after["row_count"]
        )

    elif action in {
        "fill_missing_with_mean",
        "fill_missing_with_median",
    }:
        column = command["column"]

        summary["column"] = column
        summary["missing_before"] = (
            before["missing_values"][column]
        )
        summary["missing_after"] = (
            after["missing_values"][column]
        )
        summary["values_filled"] = (
            summary["missing_before"]
            - summary["missing_after"]
        )

    elif action == "drop_column":
        summary["column_removed"] = command["column"]

    elif action == "rename_column":
        summary["old_name"] = command["column"]
        summary["new_name"] = command["new_name"]

    return summary


def clean_dataframe(
    dataframe: pd.DataFrame,
    instruction: str,
) -> tuple[pd.DataFrame, dict, float, dict]:

    working_dataframe = dataframe.copy()

    before_analysis = analyze_dataframe(
        working_dataframe
    )

    command, confidence = interpret_instruction(
        instruction,
        before_analysis["columns"],
    )

    validate_command(
        command,
        before_analysis,
    )

    cleaned_dataframe = execute_action(
        working_dataframe,
        command,
    )

    after_analysis = analyze_dataframe(
        cleaned_dataframe
    )

    summary = build_change_summary(
        before_analysis,
        after_analysis,
        command,
    )

    return (
        cleaned_dataframe,
        command,
        confidence,
        summary,
    )