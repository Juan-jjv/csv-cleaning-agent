from pathlib import Path
import random

import pandas as pd


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

    return sorted(variations)


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
        "keep one copy of identical rows",
        "retain a single instance of repeated records",
        "collapse matching records into one",
        "deduplicate identical entries",
        "keep the first occurrence of repeated rows",
        "remove extra copies of matching records",
        "keep only one occurrence of each record",
        "make sure each record appears only once",
        "collapse identical rows into one",
        "retain the first copy of matching records",
        "filter out extra copies of identical rows",
        "keep one row when multiple rows are identical",
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
        "keep only complete rows",
        "retain fully populated records",
        "exclude incomplete observations",
        "discard rows with null fields",
        "omit records with unanswered fields",
        "keep rows where every field has a value",
        "remove observations with unavailable data",
        "keep only rows with all values present",

        "filter incomplete rows out of the table",
        "leave incomplete records out of the result",
        "exclude rows that contain missing fields",
        "filter records with missing values from the dataset",
        "remove incomplete entries from the table",
        "leave records with blank fields out of the output",
        "exclude incomplete records from the result",
        "filter out observations with missing information",
        "omit rows that are not fully populated",
        "leave out rows where any field is empty",
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
        "use the arithmetic mean for gaps in COLUMN",
        "substitute missing COLUMN values with the average",
        "impute missing values in COLUMN using its mean",
        "complete gaps in COLUMN with the average",
        "calculate the average of COLUMN and use it for missing values",
        "fill absent COLUMN values using the arithmetic mean",
        "use the average value wherever COLUMN is empty",
        "replace gaps in COLUMN using its mean",
        "complete missing entries in COLUMN with the arithmetic mean",
        "impute null values in COLUMN using the average",

        "substitute blanks in COLUMN with the column mean",
        "use COLUMN's mean for missing entries",
        "calculate the column mean and fill gaps in COLUMN",
        "replace empty COLUMN values with that column's average",
        "use the mean of the COLUMN field for missing values",
        "fill missing entries in the COLUMN field with its average",

        "use the mean rather than the median for missing COLUMN values",
        "fill gaps in COLUMN with the average instead of the median",
        "use the average, not the median, for missing values in COLUMN",
        "replace missing COLUMN values with the mean rather than the median",
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
        "use the middle value for gaps in COLUMN",
        "substitute missing COLUMN values with the median",
        "impute missing values in COLUMN using its median",
        "use the central value to fill gaps in COLUMN",
        "calculate the median of COLUMN and use it for missing values",
        "fill absent COLUMN values using the middle value",
        "replace gaps in COLUMN using its median",
        "use the middle observed value when COLUMN is empty",
        "complete missing entries in COLUMN with the median",
        "impute null values in COLUMN using the central value",

        "substitute blanks in COLUMN with the column median",
        "use COLUMN's median for missing entries",
        "calculate the column median and fill gaps in COLUMN",
        "replace empty COLUMN values with that column's middle value",
        "use the median of the COLUMN field for missing values",
        "fill missing entries in the COLUMN field with its median",

        "use the median rather than the mean for missing COLUMN values",
        "fill gaps in COLUMN with the median instead of the average",
        "use the median, not the average, for missing values in COLUMN",
        "replace missing COLUMN values with the median rather than the mean",
        "do not use the average, use the median for COLUMN",
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
        "exclude COLUMN from the dataset",
        "omit the COLUMN field",
        "discard the COLUMN column",
        "take COLUMN out of the table",
        "remove COLUMN from the schema",
        "leave COLUMN out of the result",
        "produce the dataset without COLUMN",
        "get rid of the field named COLUMN",
        "COLUMN is not needed so remove it",
        "exclude the field COLUMN from the output",

        "remove the entire COLUMN field",
        "delete the field named COLUMN",
        "remove COLUMN while keeping all rows",
        "drop COLUMN but leave the other columns unchanged",
        "exclude the COLUMN column but keep the records",
        "remove only the COLUMN field",
        "take the COLUMN header and its values out of the dataset",
        "the COLUMN column should no longer exist",
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
        "label COLUMN as NEW_COLUMN",
        "give COLUMN the label NEW_COLUMN",
        "change the header from COLUMN to NEW_COLUMN",
        "relabel COLUMN as NEW_COLUMN",
        "use NEW_COLUMN as the new header for COLUMN",
        "update the COLUMN header to NEW_COLUMN",
        "call COLUMN NEW_COLUMN instead",
        "change the label of COLUMN to NEW_COLUMN",
        "make NEW_COLUMN the name of COLUMN",
        "set the COLUMN column name to NEW_COLUMN",

        "rename the field COLUMN to NEW_COLUMN",
        "label the field COLUMN as NEW_COLUMN",
        "change the field name from COLUMN to NEW_COLUMN",
        "the field COLUMN should be called NEW_COLUMN",
        "use NEW_COLUMN as the name of the field COLUMN",
        "change the COLUMN field label to NEW_COLUMN",
        "keep the field but rename COLUMN to NEW_COLUMN",
        "do not remove COLUMN, rename it to NEW_COLUMN",
        "preserve COLUMN but change its name to NEW_COLUMN",
    ]

    return add_sentence_variations(phrases)


def create_examples(
    examples: list[str],
    action: str,
) -> list[dict[str, str]]:
    return [
        {
            "instruction": instruction,
            "action": action,
        }
        for instruction in examples
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
            create_examples(
                examples,
                action,
            )
        )

    random_generator.shuffle(training_rows)

    dataframe = pd.DataFrame(training_rows)

    output_path = Path(__file__).with_name(
        "training_data.csv"
    )

    dataframe.to_csv(
        output_path,
        index=False,
    )

    print(f"Created: {output_path}")
    print(f"Total examples: {len(dataframe)}")
    print()

    print("Examples per action:")
    print(dataframe["action"].value_counts())

    print()
    print(f"Unique instructions: {dataframe['instruction'].nunique()}")


if __name__ == "__main__":
    main()