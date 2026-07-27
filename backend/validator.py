VALID_ACTIONS = {
    "remove_duplicates",
    "remove_missing_rows",
    "fill_missing_with_mean",
    "fill_missing_with_median",
    "drop_column",
    "rename_column",
}


COLUMN_ACTIONS = {
    "fill_missing_with_mean",
    "fill_missing_with_median",
    "drop_column",
    "rename_column",
}


NUMERIC_ACTIONS = {
    "fill_missing_with_mean",
    "fill_missing_with_median",
}


def validate_command(
    command: dict,
    analysis: dict,
) -> None:

    action = command.get("action")

    if action not in VALID_ACTIONS:
        raise ValueError(
            f"Unsupported action: {action}"
        )

    if action not in COLUMN_ACTIONS:
        return

    column = command.get("column")

    if column is None:
        raise ValueError(
            f"Action '{action}' requires a column."
        )

    if column not in analysis["columns"]:
        raise ValueError(
            f"Column '{column}' does not exist."
        )

    if action in NUMERIC_ACTIONS:
        if column not in analysis["numeric_columns"]:
            raise ValueError(
                f"Column '{column}' must be numeric "
                f"for action '{action}'."
            )

    if action == "rename_column":
        new_name = command.get("new_name")

        if not new_name:
            raise ValueError(
                "rename_column requires a new_name."
            )

        if (
            new_name in analysis["columns"]
            and new_name != column
        ):
            raise ValueError(
                f"Column '{new_name}' already exists."
            )