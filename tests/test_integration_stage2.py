import unittest

from calculator.api import calculate
from calculator.errors import EvalError, ParseError


class Stage2IntegrationTests(unittest.TestCase):
    def test_parse_and_evaluate_basic(self):
        self.assertAlmostEqual(calculate("1+1"), 2.0)

    def test_parse_and_evaluate_stage2_example(self):
        self.assertAlmostEqual(calculate("3.375e+09^(1/3)"), 1500.0, places=7)

    def test_parser_error_is_returned(self):
        with self.assertRaises(ParseError) as ctx:
            calculate("1 /")
        self.assertIn("Ожидалось", str(ctx.exception))

    def test_evaluator_error_is_returned(self):
        with self.assertRaises(EvalError) as ctx:
            calculate("1 / 0")
        self.assertIn("Деление на ноль", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
