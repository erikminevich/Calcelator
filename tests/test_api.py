import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from calculator.api import calculate
from calculator.errors import ParseError


ROOT = Path(__file__).resolve().parents[1]


class ApiTests(unittest.TestCase):
    def test_calculate_success(self):
        self.assertAlmostEqual(calculate("2 + 3 * 5"), 17.0)

    def test_parse_error_does_not_call_evaluator(self):
        with patch("calculator.api.evaluate") as evaluate_mock:
            with self.assertRaises(ParseError):
                calculate("2 ^ 4")
            evaluate_mock.assert_not_called()

    def test_cli_exit_code_non_zero_on_error(self):
        process = subprocess.run(
            [sys.executable, str(ROOT / "calc.py"), "2 /"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(process.returncode, 0)
        self.assertIn("Ошибка парсера", process.stderr)


if __name__ == "__main__":
    unittest.main()
