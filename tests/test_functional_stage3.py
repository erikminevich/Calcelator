import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class Stage3FunctionalTests(unittest.TestCase):
    def _run_calc(self, *args: str):
        process = subprocess.run(
            [sys.executable, str(ROOT / "calc.py"), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        return process.returncode, process.stdout.strip(), process.stderr.strip()

    def _assert_success_value(self, args: list[str], expected: float, places: int = 10):
        code, stdout, stderr = self._run_calc(*args)
        self.assertEqual(code, 0, msg=stderr)
        self.assertAlmostEqual(float(stdout), expected, places=places)

    def test_degree_sin(self):
        self._assert_success_value(["--angle-unit=degree", "sin(90)"], 1.0)

    def test_radian_sin(self):
        self._assert_success_value(["--angle-unit=radian", "sin(pi/2)"], 1.0)

    def test_default_radian_sin(self):
        self._assert_success_value(["sin(pi/2)"], 1.0)

    def test_sqrt_expression(self):
        self._assert_success_value(["sqrt(2^2 * 5 + 1)"], 4.58257569495584, places=12)

    def test_exp_ln(self):
        self._assert_success_value(["exp(ln(2))"], 2.0)

    def test_ln_exp(self):
        self._assert_success_value(["ln(exp(2))"], 2.0)

    def test_ln_e_pow_2(self):
        self._assert_success_value(["ln(e^2)"], 2.0)


if __name__ == "__main__":
    unittest.main()
