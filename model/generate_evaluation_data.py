from pathlib import Path
import csv

output_path = Path(__file__).with_name("evaluation_data.csv")

evaluation_examples = {
    "remove_duplicates": [
        "Only keep one copy when the same record occurs multiple times",
        "Some entries are repeated; keep a single instance of each",
        "Deduplicate the table so every record is unique",
        "There are repeated observations here and I only need one of each",
        "Collapse identical records down to a single row",
        "Make sure no exact record appears more than once",
        "Clean up repeated observations across the dataset",
        "Where rows are identical, retain just the first one",
        "I found the same records listed several times; keep one copy",
        "The table should contain unique records only",
        "Consolidate exact row repeats into one occurrence",
        "Strip out extra copies of identical entries",
    ],
    "remove_missing_rows": [
        "Discard any record that is incomplete",
        "Rows with at least one blank cell should not remain",
        "Keep only records where every field has a value",
        "Any observation with unavailable data can be thrown away",
        "Filter out incomplete entries from the table",
        "I only want fully populated rows",
        "Exclude records containing nulls anywhere",
        "Get the table down to rows with no gaps in their data",
        "Any row with an unanswered field should be omitted",
        "Clear out observations that are missing information",
        "Retain records only when all columns are populated",
        "Incomplete observations should be left out of the result",
    ],
    "fill_missing_with_mean": [
        "For COLUMN, use its arithmetic average wherever data is absent",
        "Impute gaps in COLUMN using the average of the available values",
        "When COLUMN is blank, substitute the column's mean",
        "Calculate COLUMN's average and put it into the missing spots",
        "Use the arithmetic mean of COLUMN to complete its gaps",
        "Missing entries for COLUMN should take the average observed value",
        "Patch absent COLUMN values with that field's mean",
        "For empty cells in COLUMN, insert the calculated average",
        "Complete COLUMN by averaging its known values and using that result for gaps",
        "Impute nulls in COLUMN with the mean calculated from nonmissing entries",
        "Where COLUMN has no value, use the average for that field",
        "Fill the holes in COLUMN using its arithmetic mean",
    ],
    "fill_missing_with_median": [
        "For COLUMN, use the middle observed value wherever data is absent",
        "Impute gaps in COLUMN using the median of its known values",
        "When COLUMN is blank, substitute the column's median",
        "Find the median for COLUMN and put it into the missing spots",
        "Use the central value of COLUMN to complete its gaps",
        "Missing entries for COLUMN should take the median observed value",
        "Patch absent COLUMN values with that field's median",
        "For empty cells in COLUMN, insert the calculated median",
        "Complete COLUMN using its median wherever values are unavailable",
        "Impute nulls in COLUMN with the median calculated from nonmissing entries",
        "Where COLUMN has no value, use the middle value for that field",
        "Fill the holes in COLUMN using its median rather than the average",
    ],
    "drop_column": [
        "COLUMN is unnecessary, so take it out of the table",
        "The result should not contain COLUMN at all",
        "Exclude COLUMN from the final dataset",
        "I do not need the field called COLUMN",
        "Leave COLUMN out when producing the cleaned table",
        "Get rid of COLUMN entirely",
        "COLUMN should be omitted from the output",
        "Take COLUMN out but leave the other fields alone",
        "The COLUMN field can be discarded",
        "Produce the data without COLUMN",
        "COLUMN is irrelevant for my analysis; take it out",
        "Remove that field named COLUMN from the schema",
    ],
    "rename_column": [
        "I want COLUMN to be called NEW_COLUMN instead",
        "Use NEW_COLUMN as the label for COLUMN",
        "The field currently named COLUMN should be labeled NEW_COLUMN",
        "Switch the header COLUMN over to NEW_COLUMN",
        "COLUMN needs a new header: NEW_COLUMN",
        "Refer to COLUMN as NEW_COLUMN from now on",
        "Update the COLUMN header so it reads NEW_COLUMN",
        "The existing COLUMN field should carry the name NEW_COLUMN",
        "Make NEW_COLUMN the new label for COLUMN",
        "Re-label COLUMN with the header NEW_COLUMN",
        "COLUMN should appear under the name NEW_COLUMN",
        "Give the existing field COLUMN the label NEW_COLUMN",
    ],
}

rows = [
    {"instruction": instruction, "action": action}
    for action, instructions in evaluation_examples.items()
    for instruction in instructions
]

with open(output_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["instruction", "action"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Created {output_path}")
print(f"Total examples: {len(rows)}")
print("Examples per action: 12")
