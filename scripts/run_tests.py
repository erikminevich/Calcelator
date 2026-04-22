import argparse
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.pretty_table import render_pretty_table  # noqa: E402


def run_unittests() -> bool:
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return result.wasSuccessful()


def _load_case_runner(stage: str):
    if stage == "stage1":
        from tests.stage1_cases import run_stage1_cases

        return run_stage1_cases
    if stage == "stage2":
        from tests.stage2_cases import run_stage2_cases

        return run_stage2_cases
    raise ValueError(stage)


def run_case_report(stage: str) -> bool:
    case_runner = _load_case_runner(stage)
    case_results = case_runner()
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

    report_path = ROOT / "reports" / f"{stage}_test_report.txt"
    print(f"\n{stage.upper()} case report")
    print(table)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(table + "\n", encoding="utf-8")

    return all(item.status == "PASS" for item in case_results)


def parse_args(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(description="Run tests and generate stage report")
    parser.add_argument("--stage", choices=["stage1", "stage2"], default="stage2")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    tests_ok = run_unittests()
    report_ok = run_case_report(args.stage)
    if tests_ok and report_ok:
        print(f"\nAll checks passed for {args.stage}.")
        return 0
    print(f"\nChecks failed for {args.stage}.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
