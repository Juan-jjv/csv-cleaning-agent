from pathlib import Path

import pandas as pd

from backend.csv_analyzer import analyze_dataframe
from backend.pipeline import clean_dataframe


def print_dataset_info(dataframe: pd.DataFrame) -> None:
    analysis = analyze_dataframe(dataframe)

    print()
    print("Dataset information")
    print("-------------------")
    print(f"Rows: {analysis['row_count']}")
    print(f"Columns: {analysis['column_count']}")
    print(f"Column names: {', '.join(analysis['columns'])}")
    print(f"Duplicate rows: {analysis['duplicate_rows']}")

    print("\nMissing values:")

    for column, count in analysis["missing_values"].items():
        print(f"  {column}: {count}")


def print_preview(dataframe: pd.DataFrame) -> None:
    print()
    print(dataframe.head(10).to_string(index=False))


def main() -> None:
    print("CSV Cleaning Agent")
    print("==================")

    csv_input = input("\nEnter CSV path: ").strip()

    csv_path = Path(csv_input)

    if not csv_path.exists():
        print(f"File does not exist: {csv_path}")
        return

    try:
        dataframe = pd.read_csv(csv_path)
    except Exception as error:
        print(f"Could not read CSV: {error}")
        return

    print(f"\nLoaded: {csv_path}")
    print_dataset_info(dataframe)
    print_preview(dataframe)

    print("\nCommands:")
    print("  :preview  Show first 10 rows")
    print("  :info     Show dataset information")
    print("  :save     Save cleaned CSV")
    print("  :quit     Exit")

    while True:
        instruction = input("\nEnter cleaning instruction: ").strip()

        if not instruction:
            continue

        if instruction == ":quit":
            print("Exiting.")
            break

        if instruction == ":preview":
            print_preview(dataframe)
            continue

        if instruction == ":info":
            print_dataset_info(dataframe)
            continue

        if instruction == ":save":
            output_path = csv_path.with_name(
                f"cleaned_{csv_path.name}"
            )

            dataframe.to_csv(
                output_path,
                index=False,
            )

            print(f"Saved cleaned CSV to: {output_path}")
            continue

        try:
            cleaned_dataframe, command = clean_dataframe(
                dataframe,
                instruction,
            )

            print("\nAI prediction:")
            for key, value in command.items():
                print(f"  {key}: {value}")

            dataframe = cleaned_dataframe

            print("\nCleaning completed.")
            print_preview(dataframe)

        except ValueError as error:
            print(f"\nCommand rejected: {error}")

        except Exception as error:
            print(f"\nUnexpected error: {error}")


if __name__ == "__main__":
    main()