import re


COLUMN_ACTIONS = {
    "fill_missing_with_mean",
    "fill_missing_with_median",
    "drop_column",
    "rename_column",
}


def _column_variants(column: str) -> list[str]:

    variants = {
        column,
        column.replace("_", " "),
        column.replace("-", " "),
    }

    return sorted(variants, key=len, reverse=True)


def _find_column_match(
    instruction: str,
    columns: list[str],
):

    candidates = []

    for column in columns:
        for variant in _column_variants(column):
            candidates.append((column, variant))

    candidates.sort(
        key=lambda item: len(item[1]),
        reverse=True,
    )

    for column, variant in candidates:
        pattern = rf"(?<!\w){re.escape(variant)}(?!\w)"

        match = re.search(
            pattern,
            instruction,
            flags=re.IGNORECASE,
        )

        if match:
            return column, match

    return None


def find_referenced_column(
    instruction: str,
    columns: list[str],
) -> str | None:

    result = _find_column_match(
        instruction,
        columns,
    )

    if result is None:
        return None

    column, _ = result

    return column


NAME_PATTERN = (
    r'(?P<new>"[^"]+"|\'[^\']+\'|[A-Za-z_][A-Za-z0-9_-]*)'
)


RENAME_PATTERNS = [
    rf"\brename\s+(?:the\s+)?(?:field\s+|column\s+)?COLUMN\s+to\s+{NAME_PATTERN}",

    rf"\bchange\s+(?:the\s+)?(?:name\s+of\s+)?COLUMN\s+to\s+{NAME_PATTERN}",

    rf"\bchange\s+(?:the\s+)?(?:header|label|name)\s+from\s+COLUMN\s+to\s+{NAME_PATTERN}",

    rf"\b(?:label|relabel)\s+(?:the\s+)?(?:field\s+)?COLUMN\s+(?:as|to)\s+{NAME_PATTERN}",

    rf"\bcall\s+COLUMN\s+{NAME_PATTERN}",

    rf"\bCOLUMN\s+(?:should\s+be|to\s+be)\s+(?:called|named|labeled)\s+{NAME_PATTERN}",

    rf"\bgive\s+COLUMN\s+(?:the\s+)?(?:new\s+)?(?:name|label)\s+{NAME_PATTERN}",

    rf"\bupdate\s+(?:the\s+)?COLUMN\s+(?:header|label|name)\s+to\s+{NAME_PATTERN}",

    rf"\b(?:use|make)\s+{NAME_PATTERN}\s+(?:as\s+)?(?:the\s+)?(?:new\s+)?(?:name|header|label)\s+(?:for|of)\s+COLUMN",
]


def _find_rename_target(
    instruction: str,
):
    for pattern in RENAME_PATTERNS:
        match = re.search(
            pattern,
            instruction,
            flags=re.IGNORECASE,
        )

        if match:
            raw_name = match.group("new")

            new_name = raw_name.strip("\"'")

            return new_name, match.span("new")

    return None


def normalize_instruction(
    instruction: str,
    columns: list[str],
) -> str:

    result = _find_column_match(
        instruction,
        columns,
    )

    if result is None:
        return instruction

    _, column_match = result

    normalized = (
        instruction[:column_match.start()]
        + "COLUMN"
        + instruction[column_match.end():]
    )

    rename_target = _find_rename_target(normalized)

    if rename_target is not None:
        _, (start, end) = rename_target

        normalized = (
            normalized[:start]
            + "NEW_COLUMN"
            + normalized[end:]
        )

    return normalized


def extract_parameters(
    instruction: str,
    columns: list[str],
    action: str,
) -> dict[str, str]:

    if action not in COLUMN_ACTIONS:
        return {}

    result = _find_column_match(
        instruction,
        columns,
    )

    if result is None:
        raise ValueError(
            "Could not determine which column the instruction refers to."
        )

    column, column_match = result

    parameters = {
        "column": column,
    }

    if action == "rename_column":
        normalized = (
            instruction[:column_match.start()]
            + "COLUMN"
            + instruction[column_match.end():]
        )

        rename_target = _find_rename_target(
            normalized
        )

        if rename_target is None:
            raise ValueError(
                "Could not determine the new column name."
            )

        new_name, _ = rename_target

        parameters["new_name"] = new_name

    return parameters