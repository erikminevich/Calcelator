from dataclasses import dataclass
from time import perf_counter
from typing import Optional

from calculator.api import calculate, format_number
from calculator.errors import EvalError, ParseError


def _sum_expr(count: int, spaced: bool) -> str:
    sep = " + " if spaced else "+"
    return sep.join(["1"] * count)


def _nested_add(levels: int) -> str:
    expr = "1"
    for _ in range(levels):
        expr = f"({expr}+1)"
    return expr


def _alternating_sum(count: int) -> str:
    terms: list[str] = []
    for i in range(count):
        if i == 0:
            terms.append("1")
        elif i % 2 == 1:
            terms.append("-1")
        else:
            terms.append("+1")
    return "".join(terms)


def _ones_product(count: int) -> str:
    return "*".join(["1"] * count)


@dataclass(frozen=True)
class LoadCase:
    case_id: str
    name: str
    expression: str
    expected_value: Optional[float] = None
    expected_error_prefix: Optional[str] = None
    threshold_ms: float = 200.0
    angle_unit: str = "radian"


@dataclass(frozen=True)
class LoadResult:
    case_id: str
    name: str
    expression: str
    expected: str
    actual: str
    time_ms: float
    threshold_ms: float
    passed: bool
    message: str


STAGE3_LOAD_CASES: list[LoadCase] = [
    LoadCase("S3-LOAD-01", "sum_250_spaced", _sum_expr(250, spaced=True), expected_value=250.0),
    LoadCase("S3-LOAD-02", "sum_500_compact", _sum_expr(500, spaced=False), expected_value=500.0),
    LoadCase("S3-LOAD-03", "sum_500_trailing_plus", _sum_expr(500, spaced=False) + "+", expected_error_prefix="Ошибка парсера"),
    LoadCase("S3-LOAD-04", "huge_numbers_sum", "1e249+1e249+1e249+1e249", expected_value=4e249),
    LoadCase("S3-LOAD-05", "one_pow_huge", "1 ^ 36893488147419103232", expected_value=1.0),
    LoadCase("S3-LOAD-06", "pow_overflow", "1.000000000000001 ^ 36893488147419103232", expected_error_prefix="Ошибка при вычислении"),
    LoadCase("S3-LOAD-07", "nested_add_120", _nested_add(120), expected_value=121.0),
    LoadCase("S3-LOAD-08", "trig_chain_50", "+".join(["sin(pi/2)"] * 50), expected_value=50.0),
    LoadCase("S3-LOAD-09", "unknown_func_large", "foo(" + ("1+" * 300) + "1)", expected_error_prefix="Ошибка при вычислении"),
    LoadCase("S3-LOAD-10", "sum_320_spaced", _sum_expr(320, spaced=True), expected_value=320.0, threshold_ms=350.0),
    LoadCase("S3-LOAD-11", "alternating_600", _alternating_sum(600), expected_value=0.0),
    LoadCase("S3-LOAD-12", "ones_product_400", _ones_product(400), expected_value=1.0),
    LoadCase("S3-LOAD-13", "lnexp_chain_80", "+".join(["ln(exp(2))"] * 80), expected_value=160.0),
    LoadCase("S3-LOAD-14", "missing_rparen_long", "(" * 90 + "1+1", expected_error_prefix="Ошибка парсера"),
    LoadCase("S3-LOAD-15", "nested_add_140", _nested_add(140), expected_value=141.0, threshold_ms=350.0),
]


def run_stage3_load_cases() -> list[LoadResult]:
    results: list[LoadResult] = []

    for case in STAGE3_LOAD_CASES:
        expected = case.expected_error_prefix or format_number(case.expected_value or 0.0)

        start = perf_counter()
        try:
            value = calculate(case.expression, angle_unit=case.angle_unit)
            time_ms = (perf_counter() - start) * 1000.0
            actual = format_number(value)

            if case.expected_error_prefix is not None:
                passed = False
                message = "Ожидалась ошибка, получен результат"
            else:
                value_ok = abs(value - float(case.expected_value)) <= 1e-9
                time_ok = time_ms <= case.threshold_ms
                passed = value_ok and time_ok
                if not value_ok:
                    message = "Некорректное значение"
                elif not time_ok:
                    message = f"Превышен порог времени ({time_ms:.2f}ms > {case.threshold_ms:.0f}ms)"
                else:
                    message = "OK"
        except ParseError as exc:
            time_ms = (perf_counter() - start) * 1000.0
            actual = f"Ошибка парсера: {exc}"
            prefix_ok = case.expected_error_prefix is not None and actual.startswith(case.expected_error_prefix)
            time_ok = time_ms <= case.threshold_ms
            passed = prefix_ok and time_ok
            if not prefix_ok:
                message = "Неожиданный тип ошибки"
            elif not time_ok:
                message = f"Превышен порог времени ({time_ms:.2f}ms > {case.threshold_ms:.0f}ms)"
            else:
                message = "OK"
        except EvalError as exc:
            time_ms = (perf_counter() - start) * 1000.0
            actual = f"Ошибка при вычислении: {exc}"
            prefix_ok = case.expected_error_prefix is not None and actual.startswith(case.expected_error_prefix)
            time_ok = time_ms <= case.threshold_ms
            passed = prefix_ok and time_ok
            if not prefix_ok:
                message = "Неожиданный тип ошибки"
            elif not time_ok:
                message = f"Превышен порог времени ({time_ms:.2f}ms > {case.threshold_ms:.0f}ms)"
            else:
                message = "OK"
        except Exception as exc:  # defensive guard to keep reporting stable
            time_ms = (perf_counter() - start) * 1000.0
            actual = f"Непредвиденная ошибка: {type(exc).__name__}: {exc}"
            passed = False
            message = "Неперехваченное исключение"

        results.append(
            LoadResult(
                case_id=case.case_id,
                name=case.name,
                expression=case.expression,
                expected=expected,
                actual=actual,
                time_ms=time_ms,
                threshold_ms=case.threshold_ms,
                passed=passed,
                message=message,
            )
        )

    return results
