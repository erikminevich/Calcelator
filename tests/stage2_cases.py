from calculator.ast_nodes import BinaryOpNode, NumberNode

from .report_helpers import ReportResult, run_evaluator_case, run_integration_case, run_parser_case


def run_stage2_parser_cases() -> list[ReportResult]:
    return [
        run_parser_case("42", "42"),
        run_parser_case("2 + 3", "Add(2, 3)"),
        run_parser_case("5 ^ 4", "Pow(5, 4)"),
        run_parser_case("1e+03", "1000"),
        run_parser_case("1 + 2 / (3 + 4)", "Add(1, Div(2, Add(3, 4)))"),
        run_parser_case("2 ^ 3 ^ 2", "Pow(2, Pow(3, 2))"),
        run_parser_case("1e+", "Ошибка парсера", expected_error="Некорректная экспонента"),
        run_parser_case("1 + (2", "Ошибка парсера", expected_error="Ожидалась ')'"),
    ]


def run_stage2_evaluator_cases() -> list[ReportResult]:
    return [
        run_evaluator_case("Pow(5, 4)", BinaryOpNode("^", NumberNode(5), NumberNode(4)), "625"),
        run_evaluator_case("Div(1e+03, 500)", BinaryOpNode("/", NumberNode(1e3), NumberNode(500)), "2"),
        run_evaluator_case(
            "Div(1, Sub(2, 2))",
            BinaryOpNode("/", NumberNode(1), BinaryOpNode("-", NumberNode(2), NumberNode(2))),
            "Ошибка при вычислении: Деление на ноль",
        ),
        run_evaluator_case(
            "Pow(1.000000000000001, 36893488147419103232)",
            BinaryOpNode("^", NumberNode(1.000000000000001), NumberNode(36893488147419103232.0)),
            "Ошибка при вычислении: Численное переполнение",
        ),
    ]


def run_stage2_integration_cases() -> list[ReportResult]:
    return [
        run_integration_case("1 + 1", "2"),
        run_integration_case("2 * 3", "6"),
        run_integration_case("2 ^ 3", "8"),
        run_integration_case("2 + (3 * 4)", "14"),
        run_integration_case("3.375e+09^(1/3)", "1500"),
        run_integration_case("1 /", "Ошибка парсера: Ожидалось число, идентификатор или '(' в позиции 3"),
        run_integration_case("1 / 0", "Ошибка при вычислении: Деление на ноль"),
    ]
