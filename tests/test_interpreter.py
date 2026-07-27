import pytest

from model.interpreter import (
    interpret_instruction,
    predict_action,
    predict_action_with_confidence,
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

def test_reject_low_confidence_prediction():
    columns = [
        "name",
        "age",
    ]

    with pytest.raises(
        ValueError,
        match="confidence is too low",
    ):
        interpret_instruction(
            "Remove duplicate rows",
            columns,
            min_confidence=1.0,
        )

def test_interpret_mean():
    columns = [
        "name",
        "salary",
    ]

    command, confidence = interpret_instruction(
        "Fill missing salary values with the mean",
        columns,
    )

    assert command == {
        "action": "fill_missing_with_mean",
        "column": "salary",
    }

    assert 0 <= confidence <= 1


def test_interpret_drop_column():
    columns = [
        "name",
        "age",
        "salary",
    ]

    command, confidence = interpret_instruction(
        "Remove the salary column",
        columns,
    )

    assert command == {
        "action": "drop_column",
        "column": "salary",
    }

    assert 0 <= confidence <= 1


def test_interpret_rename_column():
    columns = [
        "employee_id",
        "name",
    ]

    command, confidence = interpret_instruction(
        "Rename employee_id to worker_id",
        columns,
    )

    assert command == {
        "action": "rename_column",
        "column": "employee_id",
        "new_name": "worker_id",
    }

    assert 0 <= confidence <= 1