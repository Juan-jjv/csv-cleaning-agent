import pandas as pd

from backend.csv_analyzer import analyze_dataframe
from backend.executor import execute_action
from backend.validator import validate_command
from model.interpreter import interpret_instruction


def clean_dataframe(
    dataframe: pd.DataFrame,
    instruction: str,
) -> tuple[pd.DataFrame, dict]:

    working_dataframe = dataframe.copy()
    analysis = analyze_dataframe(working_dataframe)
    command = interpret_instruction(
        instruction,
        analysis["columns"],
    )

    validate_command(
        command,
        analysis,
    )

    cleaned_dataframe = execute_action(
        working_dataframe,
        command,
    )

    return cleaned_dataframe, command