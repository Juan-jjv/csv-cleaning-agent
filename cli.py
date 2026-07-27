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


def print_change_summary(
    command: dict,
    summary: dict,
) -> None:
    action = command["action"]

    print("\nChanges:")

    if action in {
        "remove_duplicates",
        "remove_missing_rows",
    }:
        print(f"  Rows before: {summary['rows_before']}")
        print(f"  Rows after: {summary['rows_after']}")
        print(f"  Rows removed: {summary['rows_removed']}")

    elif action in {
        "fill_missing_with_mean",
        "fill_missing_with_median",
    }:
        print(f"  Column: {summary['column']}")
        print(f"  Missing before: {summary['missing_before']}")
        print(f"  Missing after: {summary['missing_after']}")
        print(f"  Values filled: {summary['values_filled']}")

    elif action == "drop_column":
        print(f"  Removed column: {summary['column_removed']}")

    elif action == "rename_column":
        print(
            f"  Renamed {summary['old_name']} "
            f"to {summary['new_name']}"
        )


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
        instruction = input(
            "\nEnter cleaning instruction: "
        ).strip()

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

            print(
                f"Saved cleaned CSV to: "
                f"{output_path}"
            )

            continue

        try:
            (
                cleaned_dataframe,
                command,
                confidence,
                summary,
            ) = clean_dataframe(
                dataframe,
                instruction,
            )

            print("\nAI prediction:")

            for key, value in command.items():
                print(f"  {key}: {value}")

            print(
                f"  confidence: "
                f"{confidence:.1%}"
            )

            print_change_summary(
                command,
                summary,
            )

            dataframe = cleaned_dataframe

            print("\nCleaning completed.")

            print_preview(dataframe)

        except ValueError as error:
            print(
                f"\nCommand rejected: "
                f"{error}"
            )

        except Exception as error:
            print(
                f"\nUnexpected error: "
                f"{error}"
            )


if __name__ == "__main__":
    main()