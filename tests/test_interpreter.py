from model.interpreter import (
    interpret_instruction,
    predict_action,
)


def test_predict_remove_duplicates():
    columns = [
        "name",
        "age",
    ]

    result = predict_action(
        "Remove duplicate rows",
        columns,
    )

    assert result == "remove_duplicates"


def test_interpret_mean():
    columns = [
        "name",
        "salary",
    ]

    result = interpret_instruction(
        "Fill missing salary values with the mean",
        columns,
    )

    assert result == {
        "action": "fill_missing_with_mean",
        "column": "salary",
    }


def test_interpret_drop_column():
    columns = [
        "name",
        "age",
        "salary",
    ]

    result = interpret_instruction(
        "Remove the salary column",
        columns,
    )

    assert result == {
        "action": "drop_column",
        "column": "salary",
    }


def test_interpret_rename_column():
    columns = [
        "employee_id",
        "name",
    ]

    result = interpret_instruction(
        "Rename employee_id to worker_id",
        columns,
    )

    assert result == {
        "action": "rename_column",
        "column": "employee_id",
        "new_name": "worker_id",
    }