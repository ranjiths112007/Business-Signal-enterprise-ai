import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.business import customer_risk


def main():
    with open(os.path.join(os.path.dirname(__file__), "questions.json"), encoding="utf-8") as f:
        cases = json.load(f)
    passed = 0
    for case in cases:
        result = customer_risk(case["customer_id"])
        actual = result.get("risk_level")
        ok = actual == case["expected"]
        passed += ok
        print(f"{case['id']}: {'PASS' if ok else 'FAIL'} expected={case['expected']} actual={actual}")
    print(f"Result: {passed}/{len(cases)} passed")
    raise SystemExit(0 if passed == len(cases) else 1)


if __name__ == "__main__":
    main()
