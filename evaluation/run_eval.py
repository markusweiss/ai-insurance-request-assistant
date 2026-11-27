import json
from pathlib import Path

from app.schemas import RequestAnalysisInput
from app.services.analyzer import MistralAnalyzer

CASES_FILE = Path(__file__).parent / "llmcases.json"
FIELDS = ["urgency", "policy_number", "has_missing_information"]


def normalize(value: str | None) -> str | None:
    # Ignore whitespace and case when comparing policy numbers.
    return value.strip().upper() if value else None


def evaluate_case(analyzer: MistralAnalyzer, case: dict) -> dict:
    request = RequestAnalysisInput(subject=case["subject"], message=case["message"])
    result = analyzer.analyze(request)
    expected = case["expected"]

    actual = {
        "urgency": result.urgency.value,
        "policy_number": normalize(result.extracted_information.policy_number),
        "has_missing_information": bool(result.missing_information),
    }
    wanted = {
        "urgency": expected["urgency"],
        "policy_number": normalize(expected["policy_number"]),
        "has_missing_information": expected["has_missing_information"],
    }
    return {
        field: {"ok": actual[field] == wanted[field], "actual": actual[field], "wanted": wanted[field]}
        for field in FIELDS
    }


def main() -> None:
    cases = json.loads(CASES_FILE.read_text(encoding="utf-8"))
    analyzer = MistralAnalyzer()
    hits = {field: 0 for field in FIELDS}
    evaluated = 0

    for case in cases:
        print(f"\n{case['id']}")
        try:
            checks = evaluate_case(analyzer, case)
        except Exception as exc:
            print(f"  FEHLER: {exc}")
            continue

        evaluated += 1
        for field, check in checks.items():
            if check["ok"]:
                hits[field] += 1
                print(f"  OK    {field}")
            else:
                print(f"  FALSCH {field}: erwartet={check['wanted']!r}, erhalten={check['actual']!r}")

    print("\n--- Ergebnis ---")
    print(f"Ausgewertete Fälle: {evaluated} von {len(cases)}")
    for field in FIELDS:
        print(f"{field}: {hits[field]}/{evaluated}")


if __name__ == "__main__":
    main()