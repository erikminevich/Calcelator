from calculator.ast_nodes import BinaryOpNode, NumberNode

from .report_helpers import ReportResult, run_evaluator_case, run_integration_case, run_parser_case


def run_stage1_parser_cases() -> list[ReportResult]:
    return [
        run_parser_case("42", "42"),
        run_parser_case("3.14", "3.14"),
        run_parser_case("2 + 3", "Add(2, 3)"),
        run_parser_case("5 * 6", "Mult(5, 6)"),
        run_parser_case("10 - 4 / 2", "Sub(10, Div(4, 2))"),
        run_parser_case("0.25 / 0.001 + 0.081 * 25", "Add(Div(0.25, 0.001), Mult(0.081, 25))"),
        run_parser_case("1 + 4j", "Ошибка парсера", expected_error="Лишний токен"),
        run_parser_case("1 1 + 1", "Ошибка парсера", expected_error="Лишний токен"),
        run_parser_case("2 /", "Ошибка парсера", expected_error="Ожидалось"),
    ]


def run_stage1_evaluator_cases() -> list[ReportResult]:
    return [
        run_evaluator_case("Add(2, 2)", BinaryOpNode("+", NumberNode(2), NumberNode(2)), "4"),
        run_evaluator_case("Mult(3, 4)", BinaryOpNode("*", NumberNode(3), NumberNode(4)), "12"),
        run_evaluator_case("Div(10, 2)", BinaryOpNode("/", NumberNode(10), NumberNode(2)), "5"),
        run_evaluator_case("Sub(10, 5)", BinaryOpNode("-", NumberNode(10), NumberNode(5)), "5"),
        run_evaluator_case(
            "Div(2, 0)",
            BinaryOpNode("/", NumberNode(2), NumberNode(0)),
            "Ошибка при вычислении: Деление на ноль",
        ),
        run_evaluator_case(
            "Div(1e300, 1e-300)",
            BinaryOpNode("/", NumberNode(1e300), NumberNode(1e-300)),
            "Ошибка при вычислении: Численное переполнение",
        ),
    ]


def run_stage1_integration_cases() -> list[ReportResult]:
    return [
        run_integration_case("1 + 1", "2"),
        run_integration_case("2 * 3", "6"),
        run_integration_case("10 / 2", "5"),
        run_integration_case("1 / 0", "Ошибка при вычислении: Деление на ноль"),
        run_integration_case("1 + 4j", "Ошибка парсера: Лишний токен 'j' в позиции 5"),
    ]
