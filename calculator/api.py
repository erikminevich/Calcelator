from .evaluator import evaluate
from .parser import parse


def calculate(expression: str, angle_unit: str = "radian") -> float:
    return evaluate(parse(expression), angle_unit=angle_unit)


def format_number(value: float) -> str:
    return f"{value:.15g}"
