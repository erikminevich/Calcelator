import statistics
import sys
from pathlib import Path
from time import perf_counter


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from calculator.api import calculate  # noqa: E402
from scripts.pretty_table import render_pretty_table  # noqa: E402


def _sum_expr(count: int) -> str:
    return "+".join(["1"] * count)


def _percentile(values: list[float], p: float) -> float:
    ordered = sorted(values)
    idx = int((len(ordered) - 1) * p)
    return ordered[idx]


def benchmark_case(name: str, expression: str, iterations: int, angle_unit: str = "radian") -> list[str]:
    times_ms: list[float] = []
    for _ in range(iterations):
        start = perf_counter()
        calculate(expression, angle_unit=angle_unit)
        times_ms.append((perf_counter() - start) * 1000.0)

    avg_ms = statistics.fmean(times_ms)
    p95_ms = _percentile(times_ms, 0.95)
    max_ms = max(times_ms)
    throughput = 1000.0 / avg_ms if avg_ms > 0 else float("inf")

    return [
        name,
        str(iterations),
        f"{len(expression)}",
        f"{avg_ms:.4f}",
        f"{p95_ms:.4f}",
        f"{max_ms:.4f}",
        f"{throughput:.1f}",
    ]


def main() -> int:
    scenarios = [
        ("Сумма 100 единиц", _sum_expr(100), 6000, "radian"),
        ("Сумма 500 единиц", _sum_expr(500), 2000, "radian"),
        ("Смешанный Stage 2", "3.375e+09^(1/3)+1", 4000, "radian"),
        ("Тригонометрия (градусы)", "sin(90)+cos(0)+tg(45)", 6000, "degree"),
        ("Композиция функций", "sqrt(2^2 * 5 + 1)+ln(exp(2))", 5000, "radian"),
    ]

    rows = [benchmark_case(*scenario) for scenario in scenarios]
    headers = [
        "Сценарий",
        "Запусков",
        "Длина выражения",
        "Среднее время (мс)",
        "95-й перцентиль (мс)",
        "Макс. время (мс)",
        "Скорость (оп/с)",
    ]

    table = render_pretty_table(headers, rows)
    output_path = ROOT / "reports" / "benchmark_output.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(table + "\n", encoding="utf-8")

    print(table)
    print(f"\nОтчет benchmark сохранен: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
