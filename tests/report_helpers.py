from dataclasses import dataclass

from calculator.api import calculate, format_number
from calculator.ast_nodes import BinaryOpNode, FunctionCallNode, NumberNode
from calculator.errors import EvalError, ParseError
from calculator.evaluator import evaluate
from calculator.parser import parse


OP_NAME = {
    "+": "Add",
    "-": "Sub",
    "*": "Mult",
    "/": "Div",
    "^": "Pow",
}


@dataclass(frozen=True)
class ReportResult:
    input_value: str
    expected: str
    actual: str
    passed: bool

    @property
    def status(self) -> str:
        return "Тест пройден" if self.passed else "Тест не пройден"


def _format_number(value: float) -> str:
    rounded = round(value)
    if abs(value - rounded) < 1e-12:
        return str(int(rounded))
    return format_number(value)


def format_ast(node) -> str:
    if isinstance(node, NumberNode):
        return _format_number(node.value)

    if isinstance(node, BinaryOpNode):
        op = OP_NAME.get(node.op, node.op)
        return f"{op}({format_ast(node.left)}, {format_ast(node.right)})"

    if isinstance(node, FunctionCallNode):
        return f"{node.name}({format_ast(node.argument)})"

    return str(node)


def run_parser_case(expression: str, expected: str, expected_error: str | None = None) -> ReportResult:
    try:
        actual_ast = format_ast(parse(expression))
        if expected_error is not None:
            return ReportResult(expression, expected, actual_ast, False)
        return ReportResult(expression, expected, actual_ast, actual_ast == expected)
    except ParseError as exc:
        actual_error = f"Ошибка парсера: {exc}"
        if expected_error is None:
            return ReportResult(expression, expected, actual_error, False)
        return ReportResult(expression, expected, actual_error, expected_error in actual_error)


def run_evaluator_case(tree_label: str, node, expected: str, angle_unit: str = "radian") -> ReportResult:
    try:
        actual_value = _format_number(evaluate(node, angle_unit=angle_unit))
        return ReportResult(tree_label, expected, actual_value, actual_value == expected)
    except EvalError as exc:
        actual_error = f"Ошибка при вычислении: {exc}"
        return ReportResult(tree_label, expected, actual_error, expected == actual_error)


def run_integration_case(expression: str, expected: str, angle_unit: str = "radian") -> ReportResult:
    try:
        actual_value = _format_number(calculate(expression, angle_unit=angle_unit))
        return ReportResult(expression, expected, actual_value, actual_value == expected)
    except (ParseError, EvalError) as exc:
        if isinstance(exc, ParseError):
            actual_error = f"Ошибка парсера: {exc}"
        else:
            actual_error = f"Ошибка при вычислении: {exc}"
        return ReportResult(expression, expected, actual_error, expected == actual_error)
