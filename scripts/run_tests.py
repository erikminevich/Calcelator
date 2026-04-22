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


def _section_table(title: str, input_col: str, results) -> str:
    rows = [[item.input_value, item.expected, item.actual, item.status] for item in results]
    table = render_pretty_table([input_col, "Ожидаемый результат", "Полученный результат", "Статус"], rows)
    return f"{title}:\n{table}"


def _stage_sections(stage: str):
    if stage == "stage1":
        from tests.stage1_cases import run_stage1_evaluator_cases, run_stage1_integration_cases, run_stage1_parser_cases

        return [
            ("Тесты для парсера", "Введенное выражение", run_stage1_parser_cases()),
            ("Тесты для вычислителя", "Дерево выражений", run_stage1_evaluator_cases()),
            ("Интеграционные тесты", "Выражение", run_stage1_integration_cases()),
        ]

    if stage == "stage2":
        from tests.stage2_cases import run_stage2_evaluator_cases, run_stage2_integration_cases, run_stage2_parser_cases

        return [
            ("Тесты для парсера", "Введенное выражение", run_stage2_parser_cases()),
            ("Тесты для вычислителя", "Дерево выражений", run_stage2_evaluator_cases()),
            ("Интеграционные тесты", "Выражение", run_stage2_integration_cases()),
        ]

    if stage == "stage3":
        from tests.stage3_cases import (
            run_stage3_angle_cases,
            run_stage3_evaluator_cases,
            run_stage3_functional_cases,
            run_stage3_integration_cases,
            run_stage3_parser_cases,
        )

        return [
            ("Тесты для парсера", "Введенное выражение", run_stage3_parser_cases()),
            ("Тесты для вычислителя", "Дерево выражений", run_stage3_evaluator_cases()),
            ("Интеграционные тесты", "Выражение", run_stage3_integration_cases()),
            ("Функциональные тесты CLI", "Команда", run_stage3_functional_cases()),
            ("Тесты для единиц измерения углов", "Выражение", run_stage3_angle_cases()),
        ]

    raise ValueError(stage)


def _render_stage_report(stage: str) -> bool:
    sections = _stage_sections(stage)
    text_parts = []
    all_passed = True

    for title, input_col, results in sections:
        text_parts.append(_section_table(title, input_col, results))
        all_passed = all_passed and all(item.passed for item in results)

    report_text = "\n\n".join(text_parts) + "\n"
    report_path = ROOT / "reports" / f"{stage}_test_report.txt"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_text, encoding="utf-8")

    print(f"\nОтчет по {stage} сохранен: {report_path}")
    print(report_text)
    return all_passed


def _render_stage3_load_report() -> bool:
    from tests.stage3_load_cases import run_stage3_load_cases

    results = run_stage3_load_cases()
    lines = ["Нагрузочные тесты Stage 3", ""]

    for index, item in enumerate(results, start=1):
        lines.append(f"[{index}] {item.case_id} - {item.name}")
        lines.append(f"Входная строка: {item.expression}")
        lines.append(f"Ожидаемый результат: {item.expected}")
        lines.append(f"Полученный результат: {item.actual}")
        lines.append(f"Время выполнения: {item.time_ms:.2f} ms")
        lines.append(f"Порог времени: {item.threshold_ms:.0f} ms")
        lines.append(f"Статус: {'Тест пройден' if item.passed else 'Тест не пройден'}")
        lines.append(f"Комментарий: {item.message}")
        lines.append("-" * 80)

    report_text = "\n".join(lines) + "\n"
    report_path = ROOT / "reports" / "stage3_load_report.txt"
    report_path.write_text(report_text, encoding="utf-8")

    passed = all(item.passed for item in results)
    print(f"\nНагрузочный отчет Stage 3 сохранен: {report_path}")
    for item in results:
        status = "OK" if item.passed else "FAIL"
        print(f"{item.case_id} | {item.name} | {item.time_ms:.2f} ms | {status}")

    return passed


def parse_args(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(description="Run tests and generate stage report")
    parser.add_argument("--stage", choices=["stage1", "stage2", "stage3"], default="stage3")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    tests_ok = run_unittests()
    report_ok = _render_stage_report(args.stage)

    load_ok = True
    if args.stage == "stage3":
        load_ok = _render_stage3_load_report()

    if tests_ok and report_ok and load_ok:
        print(f"\nВсе проверки для {args.stage} пройдены.")
        return 0

    print(f"\nЕсть ошибки в проверках для {args.stage}.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
