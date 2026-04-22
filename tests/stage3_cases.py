import math
import subprocess
import sys
from pathlib import Path

from calculator.ast_nodes import BinaryOpNode, FunctionCallNode, NumberNode

from .report_helpers import ReportResult, run_evaluator_case, run_integration_case, run_parser_case


ROOT = Path(__file__).resolve().parents[1]


def run_stage3_parser_cases() -> list[ReportResult]:
    return [
        run_parser_case("pi", "3.14159265358979"),
        run_parser_case("e", "2.71828182845905"),
        run_parser_case("sqrt(4)", "sqrt(4)"),
        run_parser_case("sin(pi/2)", "sin(Div(3.14159265358979, 2))"),
        run_parser_case("ln(e^2)", "ln(Pow(2.71828182845905, 2))"),
        run_parser_case("exp(ln(2))", "exp(ln(2))"),
        run_parser_case("a + 1", "Ошибка парсера", expected_error="Неизвестный идентификатор"),
        run_parser_case("2 /", "Ошибка парсера", expected_error="Ожидалось"),
    ]


def run_stage3_evaluator_cases() -> list[ReportResult]:
    return [
        run_evaluator_case("pi", NumberNode(math.pi), "3.14159265358979"),
        run_evaluator_case("e", NumberNode(math.e), "2.71828182845905"),
        run_evaluator_case("sqrt(4)", FunctionCallNode("sqrt", NumberNode(4)), "2"),
        run_evaluator_case("sin(Div(pi, 2))", FunctionCallNode("sin", BinaryOpNode("/", NumberNode(math.pi), NumberNode(2))), "1"),
        run_evaluator_case(
            "ln(Pow(e, 2))",
            FunctionCallNode("ln", BinaryOpNode("^", NumberNode(math.e), NumberNode(2))),
            "2",
        ),
        run_evaluator_case(
            "ctg(0)",
            FunctionCallNode("ctg", NumberNode(0)),
            "Ошибка при вычислении: Деление на ноль в ctg",
        ),
    ]


def run_stage3_integration_cases() -> list[ReportResult]:
    return [
        run_integration_case("1 + 1", "2"),
        run_integration_case("3.375e+09^(1/3)", "1500"),
        run_integration_case("sqrt(ln(e))", "1"),
        run_integration_case("sin(pi/2)", "1"),
        run_integration_case("exp(ln(2))", "2"),
        run_integration_case("ln(e^2)", "2"),
        run_integration_case("a + 1", "Ошибка парсера: Неизвестный идентификатор 'a' в позиции 0"),
        run_integration_case("1 / 0", "Ошибка при вычислении: Деление на ноль"),
    ]


def run_stage3_angle_cases() -> list[ReportResult]:
    return [
        run_integration_case("sin(90)", "1", angle_unit="degree"),
        run_integration_case("sin(pi/2)", "1", angle_unit="radian"),
        run_integration_case("cos(0)", "1", angle_unit="degree"),
        run_integration_case("cos(0)", "1", angle_unit="radian"),
        run_integration_case("tg(45)", "1", angle_unit="degree"),
        run_integration_case("ctg(45)", "1", angle_unit="degree"),
    ]


def _run_cli(args: list[str]) -> tuple[int, str]:
    process = subprocess.run(
        [sys.executable, str(ROOT / "calc.py"), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    out = process.stdout.strip() if process.returncode == 0 else process.stderr.strip()
    return process.returncode, out


def run_stage3_functional_cases() -> list[ReportResult]:
    cases = [
        (["--angle-unit=degree", "sin(90)"], "1"),
        (["--angle-unit=radian", "sin(pi/2)"], "1"),
        (["sin(pi/2)"], "1"),
        (["sqrt(2^2 * 5 + 1)"], "4.58257569495584"),
        (["exp(ln(2))"], "2"),
        (["ln(exp(2))"], "2"),
        (["ln(e^2)"], "2"),
    ]

    results: list[ReportResult] = []
    for argv, expected in cases:
        code, output = _run_cli(argv)
        input_value = "calc " + " ".join(argv)
        if code == 0:
            passed = output == expected
            actual = output
        else:
            passed = False
            actual = output
        results.append(ReportResult(input_value, expected, actual, passed))

    return results
