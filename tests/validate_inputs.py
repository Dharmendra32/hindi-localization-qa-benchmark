
import csv
import json
from pathlib import Path

# Find the main project folder
PROJECT_DIR = Path(__file__).resolve().parents[1]

SOURCE_FILE = PROJECT_DIR / "input" / "source.csv"
GLOSSARY_FILE = PROJECT_DIR / "input" / "glossary.json"
REFERENCE_FILE = PROJECT_DIR / "reference" / "expected_output.json"

ALLOWED_ERRORS = {
    "TERMINOLOGY",
    "MEANING",
    "OMISSION",
    "ADDITION",
    "GRAMMAR",
    "FORMAT"
}


def validate_inputs():
    errors = []

    # 1. Validate source CSV
    with open(SOURCE_FILE, encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        required_columns = {"id", "source", "mt"}

        if set(reader.fieldnames or []) != required_columns:
            errors.append("CSV columns are incorrect.")

        source_rows = list(reader)

    source_ids = [row["id"] for row in source_rows]

    if len(source_ids) != len(set(source_ids)):
        errors.append("Duplicate IDs found in source.csv.")

    for row in source_rows:
        if not all(row.get(field, "").strip()
                   for field in ("id", "source", "mt")):
            errors.append(f"Missing data in source record: {row}")
    
    # 2. Validate glossary JSON
    with open(GLOSSARY_FILE, encoding="utf-8") as file:
        glossary = json.load(file)

    if not isinstance(glossary, dict) or not glossary:
        errors.append("Glossary must be a non-empty JSON object.")
    else:
        for term, translation in glossary.items():
            if not isinstance(term, str) or not isinstance(translation, str):
                errors.append("Glossary terms and translations must be strings.")
            elif not term.strip() or not translation.strip():
                errors.append("Glossary contains an empty term or translation.")

    # 3. Validate reference JSON
    with open(REFERENCE_FILE, encoding="utf-8") as file:
        reference = json.load(file)

    required_fields = {
        "id",
        "has_error",
        "error_types",
        "explanation",
        "corrected_translation"
    }

    reference_ids = []

    for record in reference:
        if not isinstance(record, dict):
            errors.append("A reference record is not a JSON object.")
            continue

        if not required_fields.issubset(record.keys()):
            errors.append(f"Missing fields in reference record: {record}")
            continue

        reference_ids.append(record["id"])

        if not isinstance(record["has_error"], bool):
            errors.append(f"Invalid has_error value for ID {record['id']}.")

        if not isinstance(record["error_types"], list):
            errors.append(f"error_types must be a list for ID {record['id']}.")
        else:
            invalid_types = set(record["error_types"]) - ALLOWED_ERRORS
            if invalid_types:
                errors.append(f"Invalid error categories for ID {record['id']}.")

            if record["has_error"] != bool(record["error_types"]):
                errors.append(f"has_error does not match error_types for ID {record['id']}.")

        if not isinstance(record["explanation"], str) or not record["explanation"].strip():
            errors.append(f"Missing explanation for ID {record['id']}.")

        if not isinstance(record["corrected_translation"], str) or not record["corrected_translation"].strip():
            errors.append(f"Missing correction for ID {record['id']}.")

    if len(reference_ids) != len(set(reference_ids)):
        errors.append("Duplicate IDs found in expected_output.json.")

    if set(source_ids) != set(reference_ids):
        errors.append("Source IDs and reference IDs do not match.")

    # 4. Print validation results
    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print("-", error)
    else:
        print("ALL VALIDATIONS PASSED")
        print("Source records:", len(source_rows))
        print("Glossary terms:", len(glossary))
        print("Reference records:", len(reference))
        print("Source and reference IDs match.")


if __name__ == "__main__":
    validate_inputs()
