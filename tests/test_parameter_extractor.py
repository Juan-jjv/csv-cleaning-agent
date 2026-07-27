from model.parameter_extractor import (
    extract_parameters,
    find_referenced_column,
    normalize_instruction,
)


def test_find_referenced_column():
    columns = [
        "name",
        "age",
        "salary",
    ]

    result = find_referenced_column(
        "Fill missing age values with the median",
        columns,
    )

    assert result == "age"


def test_column_with_underscore():
    columns = [
        "employee_id",
        "salary",
    ]

    result = find_referenced_column(
        "Remove the employee id column",
        columns,
    )

    assert result == "employee_id"


def test_normalize_instruction():
    columns = [
        "pressure_kpa",
        "temperature",
    ]

    result = normalize_instruction(
        "Fill missing pressure_kpa values with the median",
        columns,
    )

    assert result == (
        "Fill missing COLUMN values with the median"
    )


def test_extract_column_parameter():
    columns = [
        "age",
        "salary",
    ]

    result = extract_parameters(
        "Fill missing salary values with the mean",
        columns,
        "fill_missing_with_mean",
    )

    assert result == {
        "column": "salary",
    }


def test_extract_rename_parameters():
    columns = [
        "employee_id",
        "name",
    ]

    result = extract_parameters(
        "Rename employee_id to worker_id",
        columns,
        "rename_column",
    )

    assert result == {
        "column": "employee_id",
        "new_name": "worker_id",
    }


def test_normalize_rename_instruction():
    columns = [
        "employee_id",
        "name",
    ]

    result = normalize_instruction(
        "Rename employee_id to worker_id",
        columns,
    )

    assert result == (
        "Rename COLUMN to NEW_COLUMN"
    )


def test_action_without_parameters():
    columns = [
        "name",
        "age",
    ]

    result = extract_parameters(
        "Remove duplicate rows",
        columns,
        "remove_duplicates",
    )

    assert result == {}