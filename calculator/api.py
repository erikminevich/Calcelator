from .evaluator import evaluate
from .parser import parse


def calculate(expression: str) -> float:
    return evaluate(parse(expression))


def format_number(value: float) -> str:
    return f"{value:.15g}"
