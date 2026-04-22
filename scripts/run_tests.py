import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.pretty_table import render_pretty_table  # noqa: E402
from tests.stage1_cases import run_stage1_cases  # noqa: E402


REPORT_PATH = ROOT / "reports" / "stage1_test_report.txt"


def run_unittests() -> bool:
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return result.wasSuccessful()


def run_case_report() -> bool:
    case_results = run_stage1_cases()
    rows = [
        [
            item.stage,
            item.case_id,
            item.source,
            item.expression,
            item.expected,
            item.actual,
            item.message,
            item.status,
        ]
        for item in case_results
    ]

    table = render_pretty_table(
        ["Stage", "Case ID", "Source", "Input", "Expected", "Actual", "Message", "Status"],
        rows,
    )

    print("\nStage 1 case report")
    print(table)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(table + "\n", encoding="utf-8")

    return all(item.status == "PASS" for item in case_results)


def main() -> int:
    tests_ok = run_unittests()
    report_ok = run_case_report()
    if tests_ok and report_ok:
        print(f"\nAll checks passed. Report saved to: {REPORT_PATH}")
        return 0
    print(f"\nChecks failed. Report saved to: {REPORT_PATH}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
