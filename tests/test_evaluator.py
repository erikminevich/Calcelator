import math
import unittest

from calculator.ast_nodes import BinaryOpNode, FunctionCallNode, NumberNode
from calculator.errors import EvalError
from calculator.evaluator import evaluate


class EvaluatorTests(unittest.TestCase):
    def _apply(self, op: str, left: float, right: float) -> float:
        if op == "+":
            return left + right
        if op == "-":
            return left - right
        if op == "*":
            return left * right
        if op == "/":
            if right == 0.0:
                raise ZeroDivisionError("division by zero")
            return left / right
        if op == "^":
            return left**right
        raise ValueError(op)

    def test_all_trees_with_two_operations(self):
        ops = ["+", "-", "*", "/", "^"]
        a, b, c = 8.0, 2.0, 4.0

        for op1 in ops:
            for op2 in ops:
                with self.subTest(shape="left", op1=op1, op2=op2):
                    tree = BinaryOpNode(op2, BinaryOpNode(op1, NumberNode(a), NumberNode(b)), NumberNode(c))
                    expected = self._apply(op2, self._apply(op1, a, b), c)
                    self.assertAlmostEqual(evaluate(tree), expected)

                with self.subTest(shape="right", op1=op1, op2=op2):
                    tree = BinaryOpNode(op2, NumberNode(a), BinaryOpNode(op1, NumberNode(b), NumberNode(c)))
                    expected = self._apply(op2, a, self._apply(op1, b, c))
                    self.assertAlmostEqual(evaluate(tree), expected)

    def test_supported_functions(self):
        self.assertAlmostEqual(evaluate(FunctionCallNode("sqrt", NumberNode(9.0))), 3.0)
        self.assertAlmostEqual(evaluate(FunctionCallNode("ln", NumberNode(math.e))), 1.0)
        self.assertAlmostEqual(evaluate(FunctionCallNode("exp", NumberNode(2.0))), math.exp(2.0))

    def test_trigonometry_units(self):
        self.assertAlmostEqual(evaluate(FunctionCallNode("sin", NumberNode(math.pi / 2))), 1.0, places=12)
        self.assertAlmostEqual(
            evaluate(FunctionCallNode("sin", NumberNode(90.0)), angle_unit="degree"),
            1.0,
            places=12,
        )

    def test_division_by_zero_error(self):
        with self.assertRaises(EvalError):
            evaluate(BinaryOpNode("/", NumberNode(2.0), NumberNode(0.0)))

    def test_overflow_error(self):
        with self.assertRaises(EvalError):
            evaluate(BinaryOpNode("/", NumberNode(1e300), NumberNode(1e-300)))

    def test_function_domain_errors(self):
        with self.assertRaises(EvalError):
            evaluate(FunctionCallNode("sqrt", NumberNode(-1.0)))
        with self.assertRaises(EvalError):
            evaluate(FunctionCallNode("ln", NumberNode(0.0)))
        with self.assertRaises(EvalError):
            evaluate(FunctionCallNode("ctg", NumberNode(0.0)))

    def test_power_domain_error(self):
        with self.assertRaises(EvalError):
            evaluate(BinaryOpNode("^", NumberNode(-2.0), NumberNode(0.5)))

    def test_unknown_node_error(self):
        with self.assertRaises(EvalError):
            evaluate(object())

    def test_unsupported_operator_error(self):
        with self.assertRaises(EvalError):
            evaluate(BinaryOpNode("%", NumberNode(2.0), NumberNode(3.0)))

    def test_invalid_angle_unit(self):
        with self.assertRaises(EvalError):
            evaluate(NumberNode(1.0), angle_unit="grad")


if __name__ == "__main__":
    unittest.main()
