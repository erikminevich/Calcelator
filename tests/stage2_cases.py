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


STAGE2_CASES: list[StageCase] = [
    StageCase("S2-REQ-01", "assignment", "1.25e+09", expected_value=1250000000.0),
    StageCase("S2-REQ-02", "assignment", "3^4", expected_value=81.0),
    StageCase("S2-REQ-03", "assignment", "1 + 2 / (3 + 4)", expected_value=1.2857142857142856),
    StageCase("S2-REQ-04", "assignment", "3.375e+09^(1/3)", expected_value=1500.0),
    StageCase("S2-REQ-05", "assignment", "1 /", expected_error_prefix="Ошибка парсера"),
    StageCase("S2-REQ-06", "assignment", "1 / 0", expected_error_prefix="Ошибка при вычислении"),
    StageCase("S2-EXT-01", "extra", "2^3^2", expected_value=512.0),
    StageCase("S2-EXT-02", "extra", "(2 + 3) * (4 - 1)", expected_value=15.0),
]


def run_stage2_cases() -> list[CaseResult]:
    results: list[CaseResult] = []

    for case in STAGE2_CASES:
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
                if diff <= 1e-9:
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
                stage="stage2",
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
