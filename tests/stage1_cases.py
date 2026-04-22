from dataclasses import dataclass
from typing import Optional

from calculator.api import calculate, format_number
from calculator.errors import EvalError, ParseError


@dataclass(frozen=True)
class StageCase:
    case_id: str
    source: str
    expression: str
    expected_value: Optional[float] = None
    expected_error_prefix: Optional[str] = None


@dataclass(frozen=True)
class CaseResult:
    stage: str
    case_id: str
    source: str
    expression: str
    expected: str
    actual: str
    message: str
    status: str


STAGE1_CASES: list[StageCase] = [
    StageCase("S1-REQ-01", "assignment", "7", expected_value=7.0),
    StageCase("S1-REQ-02", "assignment", "2 + 3 * 5", expected_value=17.0),
    StageCase("S1-REQ-03", "assignment", "12 / 4 - 1", expected_value=2.0),
    StageCase("S1-REQ-04", "assignment", "2 ^ 4", expected_error_prefix="Ошибка парсера"),
    StageCase("S1-REQ-05", "assignment", "2 /", expected_error_prefix="Ошибка парсера"),
    StageCase("S1-REQ-06", "assignment", "1 + 4j", expected_error_prefix="Ошибка парсера"),
    StageCase("S1-REQ-07", "assignment", "2 / 0", expected_error_prefix="Ошибка при вычислении"),
    StageCase("S1-REQ-08", "assignment", "1 + 0.0000000000000000000001", expected_value=1.0),
    StageCase("S1-EXT-01", "extra", "1 1 + 1", expected_error_prefix="Ошибка парсера"),
    StageCase("S1-EXT-02", "extra", ".5 + .25", expected_value=0.75),
    StageCase("S1-EXT-03", "extra", "8 / 4 / 2", expected_value=1.0),
]


def run_stage1_cases() -> list[CaseResult]:
    results: list[CaseResult] = []

    for case in STAGE1_CASES:
        expected = (
            case.expected_error_prefix if case.expected_error_prefix else format_number(case.expected_value or 0.0)
        )

        try:
            value = calculate(case.expression)
            actual = format_number(value)
            if case.expected_error_prefix:
                status = "FAIL"
                message = "Ожидалась ошибка, но получен результат"
            else:
                diff = abs(value - float(case.expected_value))
                if diff <= 1e-12:
                    status = "PASS"
                    message = "OK"
                else:
                    status = "FAIL"
                    message = f"Отклонение {diff:.3g}"
        except ParseError as exc:
            actual = f"Ошибка парсера: {exc}"
            if case.expected_error_prefix and actual.startswith(case.expected_error_prefix):
                status = "PASS"
                message = "OK"
            else:
                status = "FAIL"
                message = "Неожиданная ошибка парсера"
        except EvalError as exc:
            actual = f"Ошибка при вычислении: {exc}"
            if case.expected_error_prefix and actual.startswith(case.expected_error_prefix):
                status = "PASS"
                message = "OK"
            else:
                status = "FAIL"
                message = "Неожиданная ошибка вычисления"

        results.append(
            CaseResult(
                stage="stage1",
                case_id=case.case_id,
                source=case.source,
                expression=case.expression,
                expected=expected,
                actual=actual,
                message=message,
                status=status,
            )
        )

    return results
