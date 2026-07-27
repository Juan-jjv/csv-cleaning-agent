import pytest

from backend.validator import validate_command


ANALYSIS = {
    "columns": [
        "name",
        "age",
        "salary",
    ],
    "numeric_columns": [
        "age",
        "salary",
    ],
}


def test_valid_mean_command():
    command = {
        "action": "fill_missing_with_mean",
        "column": "salary",
    }

    validate_command(
        command,
        ANALYSIS,
    )


def test_reject_non_numeric_mean():
    command = {
        "action": "fill_missing_with_mean",
        "column": "name",
    }

    with pytest.raises(ValueError):
        validate_command(
            command,
            ANALYSIS,
        )


def test_reject_missing_column():
    command = {
        "action": "drop_column",
        "column": "height",
    }

    with pytest.raises(ValueError):
        validate_command(
            command,
            ANALYSIS,
        )


def test_valid_remove_duplicates():
    command = {
        "action": "remove_duplicates",
    }

    validate_command(
        command,
        ANALYSIS,
    )


def test_valid_rename():
    command = {
        "action": "rename_column",
        "column": "age",
        "new_name": "years_old",
    }

    validate_command(
        command,
        ANALYSIS,
    )


def test_reject_existing_rename_target():
    command = {
        "action": "rename_column",
        "column": "age",
        "new_name": "salary",
    }

    with pytest.raises(ValueError):
        validate_command(
            command,
            ANALYSIS,
        )