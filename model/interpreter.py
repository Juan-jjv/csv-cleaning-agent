from functools import lru_cache
from pathlib import Path

import joblib

from model.parameter_extractor import (
    extract_parameters,
    normalize_instruction,
)


MODEL_PATH = Path(__file__).with_name("action_classifier.joblib")


@lru_cache(maxsize=1)
def load_action_classifier():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Action classifier not found. "
            "Run model/train.py first."
        )

    return joblib.load(MODEL_PATH)


def predict_action(
    instruction: str,
    columns: list[str],
) -> str:

    normalized_instruction = normalize_instruction(
        instruction,
        columns,
    )

    model = load_action_classifier()

    prediction = model.predict(
        [normalized_instruction]
    )

    return str(prediction[0])


def interpret_instruction(
    instruction: str,
    columns: list[str],
) -> dict:

    normalized_instruction = normalize_instruction(
        instruction,
        columns,
    )

    model = load_action_classifier()

    action = str(
        model.predict(
            [normalized_instruction]
        )[0]
    )

    parameters = extract_parameters(
        instruction,
        columns,
        action,
    )

    return {
        "action": action,
        **parameters,
    }