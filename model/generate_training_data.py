from pathlib import Path
import random

import pandas as pd


TARGET_PER_ACTION = 120
RANDOM_SEED = 42

random_generator = random.Random(RANDOM_SEED)


PREFIXES = [
    "",
    "Please ",
    "Can you ",
    "Could you ",
    "I need you to ",
]

SUFFIXES = [
    "",
    " in the dataset",
    " in this CSV",
    " from this file",
]


def add_sentence_variations(phrases: list[str]) -> list[str]:
    variations = set()

    for phrase in phrases:
        for prefix in PREFIXES:
            for suffix in SUFFIXES:
                sentence = f"{prefix}{phrase}{suffix}".strip()

                sentence = sentence[0].upper() + sentence[1:]

                variations.add(sentence)

    return list(variations)


def generate_remove_duplicates() -> list[str]:
    phrases = [
        "remove duplicate rows",
        "delete duplicate records",
        "remove repeated rows",
        "delete repeated entries",
        "keep only unique rows",
        "get rid of duplicated records",
        "remove rows that appear more than once",
        "eliminate duplicate entries",
    ]

    return add_sentence_variations(phrases)


def generate_remove_missing_rows() -> list[str]:
    phrases = [
        "remove rows with missing values",
        "delete rows containing missing values",
        "remove incomplete rows",
        "delete records with empty values",
        "remove rows that contain blanks",
        "drop rows with missing data",
        "get rid of incomplete records",
        "remove records that have empty fields",
    ]

    return add_sentence_variations(phrases)


def generate_fill_missing_with_mean() -> list[str]:
    phrases = [
        "fill missing values in COLUMN with the mean",
        "replace missing values in COLUMN with the average",
        "use the mean for empty values in COLUMN",
        "fill empty values in COLUMN using the average",
        "replace blank values in COLUMN with the mean",
        "use the average to fill missing values in COLUMN",
    ]

    return add_sentence_variations(phrases)


def generate_fill_missing_with_median() -> list[str]:
    phrases = [
        "fill missing values in COLUMN with the median",
        "replace missing values in COLUMN with the median",
        "use the median for empty values in COLUMN",
        "fill empty values in COLUMN using the median",
        "replace blank values in COLUMN with the median",
        "use the median to fill missing values in COLUMN",
    ]

    return add_sentence_variations(phrases)


def generate_drop_column() -> list[str]:
    phrases = [
        "remove the COLUMN column",
        "delete the COLUMN column",
        "drop the COLUMN column",
        "remove the field COLUMN",
        "get rid of COLUMN",
        "delete COLUMN",
    ]

    return add_sentence_variations(phrases)


def generate_rename_column() -> list[str]:
    phrases = [
        "rename COLUMN to NEW_COLUMN",
        "rename the COLUMN column to NEW_COLUMN",
        "change the name of COLUMN to NEW_COLUMN",
        "change COLUMN to NEW_COLUMN",
        "give COLUMN the new name NEW_COLUMN",
        "replace the name COLUMN with NEW_COLUMN",
    ]

    return add_sentence_variations(phrases)


def sample_examples(
    examples: list[str],
    action: str,
) -> list[dict[str, str]]:

    if len(examples) < TARGET_PER_ACTION:
        raise ValueError(
            f"Not enough unique examples for {action}. "
            f"Generated {len(examples)}."
        )

    selected = random_generator.sample(
        examples,
        TARGET_PER_ACTION,
    )

    return [
        {
            "instruction": instruction,
            "action": action,
        }
        for instruction in selected
    ]


def main() -> None:
    generators = {
        "remove_duplicates": generate_remove_duplicates,
        "remove_missing_rows": generate_remove_missing_rows,
        "fill_missing_with_mean": generate_fill_missing_with_mean,
        "fill_missing_with_median": generate_fill_missing_with_median,
        "drop_column": generate_drop_column,
        "rename_column": generate_rename_column,
    }

    training_rows = []

    for action, generator in generators.items():
        examples = generator()

        training_rows.extend(
            sample_examples(examples, action)
        )

    random_generator.shuffle(training_rows)

    dataframe = pd.DataFrame(training_rows)

    output_path = Path(__file__).with_name("training_data.csv")

    dataframe.to_csv(
        output_path,
        index=False,
    )

    print(f"Created: {output_path}")
    print(f"Total examples: {len(dataframe)}")
    print()
    print(dataframe["action"].value_counts())


if __name__ == "__main__":
    main()