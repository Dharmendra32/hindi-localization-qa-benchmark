
import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]

REFERENCE_FILE = PROJECT_DIR / "reference" / "expected_output.json"
SUBMISSION_FILE = PROJECT_DIR / "output" / "agent_output.json"


def load_json(path):
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def evaluate_agent():
    reference = load_json(REFERENCE_FILE)
    submission = load_json(SUBMISSION_FILE)

    reference_by_id = {item["id"]: item for item in reference}
    submission_by_id = {item["id"]: item for item in submission}

    missing_ids = set(reference_by_id) - set(submission_by_id)
    extra_ids = set(submission_by_id) - set(reference_by_id)

    results = {
        "error_detection": 0,
        "error_categories": 0,
        "corrected_translation": 0
    }

    total = len(reference)

    print("\nAI AGENT BENCHMARK EVALUATION")
    print("-----------------------------")

    for segment_id, expected in reference_by_id.items():

        actual = submission_by_id.get(segment_id)

        if actual is None:
            print(f"\nID {segment_id}: MISSING")
            continue

        detection_correct = (
            actual.get("has_error") == expected["has_error"]
        )

        categories_correct = (
            set(actual.get("error_types", []))
            == set(expected["error_types"])
        )

        correction_correct = (
            actual.get("corrected_translation")
            == expected["corrected_translation"]
        )

        results["error_detection"] += int(detection_correct)
        results["error_categories"] += int(categories_correct)
        results["corrected_translation"] += int(correction_correct)

        print(f"\nID {segment_id}")
        print("Error detection:", "PASS" if detection_correct else "FAIL")
        print("Error categories:", "PASS" if categories_correct else "FAIL")
        print("Correction:", "PASS" if correction_correct else "FAIL")

    print("\nMISSING IDs:", sorted(missing_ids))
    print("EXTRA IDs:", sorted(extra_ids))

    print("\nSCORE SUMMARY")
    print("-------------")

    for category, score in results.items():
        percentage = (score / total) * 100 if total else 0
        print(f"{category}: {score}/{total} ({percentage:.1f}%)")

    all_passed = (
        not missing_ids
        and not extra_ids
        and all(score == total for score in results.values())
    )

    print("\nFINAL RESULT:", "PASS" if all_passed else "FAIL")


if __name__ == "__main__":
    evaluate_agent()
