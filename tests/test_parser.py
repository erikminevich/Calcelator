import unittest

from calculator.ast_nodes import BinaryOpNode, NumberNode
from calculator.errors import ParseError
from calculator.parser import parse


class ParserTests(unittest.TestCase):
    def test_number_is_expression(self):
        node = parse("42")
        self.assertEqual(node, NumberNode(42.0))

    def test_scientific_notation_number(self):
        node = parse("1.25e+09")
        self.assertEqual(node, NumberNode(1.25e9))

    def test_power_is_right_associative(self):
        node = parse("2^3^2")
        self.assertEqual(
            node,
            BinaryOpNode("^", NumberNode(2.0), BinaryOpNode("^", NumberNode(3.0), NumberNode(2.0))),
        )

    def test_parentheses_change_precedence(self):
        node = parse("(1 + 2) * 3")
        self.assertEqual(
            node,
            BinaryOpNode("*", BinaryOpNode("+", NumberNode(1.0), NumberNode(2.0)), NumberNode(3.0)),
        )

    def test_operations_and_precedence(self):
        node = parse("2 + 3 * 5 - 4 / 2")

        self.assertIsInstance(node, BinaryOpNode)
        self.assertEqual(node.op, "-")
        self.assertEqual(node.right, BinaryOpNode("/", NumberNode(4.0), NumberNode(2.0)))

        left = node.left
        self.assertEqual(left, BinaryOpNode("+", NumberNode(2.0), BinaryOpNode("*", NumberNode(3.0), NumberNode(5.0))))

    def test_1_2_3_digit_numbers(self):
        node = parse("1 + 22 + 333")
        self.assertEqual(
            node,
            BinaryOpNode(
                "+",
                BinaryOpNode("+", NumberNode(1.0), NumberNode(22.0)),
                NumberNode(333.0),
            ),
        )

    def test_invalid_expressions_examples(self):
        invalid = ["2 ^^ 4", "2 /", "1 + 4j", "1 1 + 1", "1 + (2", "1e+"]
        for expr in invalid:
            with self.subTest(expr=expr):
                with self.assertRaises(ParseError):
                    parse(expr)

    def test_empty_expression(self):
        with self.assertRaises(ParseError):
            parse("   ")


if __name__ == "__main__":
    unittest.main()
