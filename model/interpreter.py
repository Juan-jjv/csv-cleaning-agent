from functools import lru_cache
from pathlib import Path

import joblib

from model.parameter_extractor import (
    extract_parameters,
    normalize_instruction,
)


MODEL_PATH = Path(__file__).with_name("action_classifier.joblib")

MIN_CONFIDENCE =  0.60


@lru_cache(maxsize=1)
def load_action_classifier():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Action classifier not found. "
            "Run model/train.py first."
        )

    return joblib.load(MODEL_PATH)


def predict_action_with_confidence(
    instruction: str,
    columns: list[str],
) -> tuple[str, float]:

    normalized_instruction = normalize_instruction(
        instruction,
        columns,
    )

    model = load_action_classifier()

    probabilities = model.predict_proba(
        [normalized_instruction]
    )[0]

    classes = model.named_steps[
        "classifier"
    ].classes_

    best_index = int(probabilities.argmax())

    action = str(classes[best_index])
    confidence = float(probabilities[best_index])

    return action, confidence


def predict_action(
    instruction: str,
    columns: list[str],
) -> str:

    action, _ = predict_action_with_confidence(
        instruction,
        columns,
    )

    return action


def interpret_instruction(
    instruction: str,
    columns: list[str],
    min_confidence: float = MIN_CONFIDENCE,
) -> tuple[dict, float]:

    if not 0 <= min_confidence <= 1:
        raise ValueError(
            "Minimum confidence must be between 0 and 1."
        )

    action, confidence = predict_action_with_confidence(
        instruction,
        columns,
    )

    if action == "unsupported":
        raise ValueError(
            "This instruction does not match a supported cleaning action."
    )

    if confidence < min_confidence:
        raise ValueError(
            f"AI prediction confidence is too low "
            f"({confidence:.1%}). "
            f"Try rephrasing the instruction."
        )

    parameters = extract_parameters(
        instruction,
        columns,
        action,
    )

    command = {
        "action": action,
        **parameters,
    }

    return command, confidence