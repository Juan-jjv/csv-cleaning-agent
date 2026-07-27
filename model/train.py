from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib


DATA_PATH = Path(__file__).with_name("training_data.csv")
MODEL_PATH = Path(__file__).with_name("action_classifier.joblib")


def load_training_data() -> pd.DataFrame:
    dataframe = pd.read_csv(DATA_PATH)

    required_columns = {"instruction", "action"}

    if not required_columns.issubset(dataframe.columns):
        raise ValueError(
            "Training data must contain 'instruction' and 'action' columns."
        )

    if dataframe["instruction"].isna().any():
        raise ValueError("Training data contains missing instructions.")

    if dataframe["action"].isna().any():
        raise ValueError("Training data contains missing action labels.")

    return dataframe


def train_model(dataframe: pd.DataFrame) -> Pipeline:
    model = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                ngram_range=(1, 2),
            ),
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
            ),
        ),
    ])

    instructions = dataframe["instruction"]
    actions = dataframe["action"]

    model.fit(instructions, actions)

    return model


def main() -> None:
    training_data = load_training_data()

    model = train_model(training_data)

    joblib.dump(model, MODEL_PATH)

    print(f"Training examples: {len(training_data)}")
    print(f"Actions: {training_data['action'].nunique()}")
    print(f"Saved model: {MODEL_PATH}")


if __name__ == "__main__":
    main()