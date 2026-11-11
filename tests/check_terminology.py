
import csv
import json
import re
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]

SOURCE_FILE = PROJECT_DIR / "input" / "source.csv"
GLOSSARY_FILE = PROJECT_DIR / "input" / "glossary.json"

# Accepted Hindi forms for terms that can change grammatically.
# These are controlled variants, not unrestricted synonyms.
APPROVED_VARIANTS = {
    "account": ["खाता", "खाते"],
}


def source_contains_term(source, term):
    """Check whether an English term occurs in the source."""
    pattern = r"(?<!\w)" + re.escape(term) + r"(?!\w)"
    return re.search(pattern, source, re.IGNORECASE) is not None


def translation_contains_term(translation, approved_forms):
    """Check whether an approved Hindi form occurs in the translation."""
    return any(form in translation for form in approved_forms)


def check_terminology():
    with open(GLOSSARY_FILE, encoding="utf-8") as file:
        glossary = json.load(file)

    with open(SOURCE_FILE, encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    violations = []

    for row in rows:
        source = row["source"]
        translation = row["mt"]
        segment_id = row["id"]

        for english_term, hindi_term in glossary.items():

            # Only check terms that occur in the English source.
            if not source_contains_term(source, english_term):
                continue

            # Use approved grammatical variants when available.
            accepted_forms = APPROVED_VARIANTS.get(
                english_term, [hindi_term]
            )

            if not translation_contains_term(
                translation, accepted_forms
            ):
                violations.append({
                    "id": segment_id,
                    "english_term": english_term,
                    "expected_hindi": hindi_term,
                    "actual_translation": translation
                })

    print("\nHINDI TERMINOLOGY CHECK")
    print("-----------------------")

    if violations:
        print("Terminology violations found:", len(violations))

        for item in violations:
            print(f"\nID: {item['id']}")
            print(f"English term: {item['english_term']}")
            print(f"Approved Hindi: {item['expected_hindi']}")
            print(f"Actual translation: {item['actual_translation']}")
    else:
        print("No terminology violations found.")

    print("\nSegments checked:", len(rows))


if __name__ == "__main__":
    check_terminology()
