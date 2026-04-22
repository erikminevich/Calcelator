import unittest

from tests.stage3_load_cases import STAGE3_LOAD_CASES, run_stage3_load_cases


class Stage3LoadTests(unittest.TestCase):
    def test_additional_load_cases_count(self):
        self.assertGreaterEqual(len(STAGE3_LOAD_CASES), 10)
        self.assertLessEqual(len(STAGE3_LOAD_CASES), 15)

    def test_stage3_load_cases(self):
        results = run_stage3_load_cases()
        failed = [
            f"{item.case_id} ({item.name}): {item.message}; actual={item.actual}; time={item.time_ms:.2f}ms"
            for item in results
            if not item.passed
        ]
        if failed:
            self.fail("\n".join(failed))


if __name__ == "__main__":
    unittest.main()
