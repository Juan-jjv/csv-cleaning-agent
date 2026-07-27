from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report


MODEL_PATH = Path(__file__).with_name("action_classifier.joblib")
EVALUATION_PATH = Path(__file__).with_name("evaluation_data.csv")


def main() -> None:
    model = joblib.load(MODEL_PATH)

    evaluation_data = pd.read_csv(EVALUATION_PATH)

    instructions = evaluation_data["instruction"]
    expected_actions = evaluation_data["action"]

    predicted_actions = model.predict(instructions)

    print("\nIncorrect predictions:\n")

    for instruction, expected, predicted in zip(
        instructions,
        expected_actions,
        predicted_actions,
    ):
        if expected != predicted:
            print(f"Instruction: {instruction}")
            print(f"Expected:    {expected}")
            print(f"Predicted:   {predicted}")
            print()

    accuracy = accuracy_score(
        expected_actions,
        predicted_actions,
    )

    print(f"Accuracy: {accuracy:.2%}")
    print()

    print(
        classification_report(
            expected_actions,
            predicted_actions,
        )
    )


if __name__ == "__main__":
    main()