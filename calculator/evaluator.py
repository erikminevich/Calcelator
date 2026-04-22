import math

from .ast_nodes import BinaryOpNode, NumberNode
from .errors import EvalError


def _ensure_finite(value: float) -> float:
    if not math.isfinite(value):
        raise EvalError("Численное переполнение")
    return value


def evaluate(node) -> float:
    if isinstance(node, NumberNode):
        return _ensure_finite(node.value)

    if not isinstance(node, BinaryOpNode):
        raise EvalError("Неизвестный узел выражения")

    left = evaluate(node.left)
    right = evaluate(node.right)

    if node.op == "+":
        return _ensure_finite(left + right)
    if node.op == "-":
        return _ensure_finite(left - right)
    if node.op == "*":
        return _ensure_finite(left * right)
    if node.op == "/":
        if right == 0.0:
            raise EvalError("Деление на ноль")
        return _ensure_finite(left / right)
    if node.op == "^":
        try:
            result = math.pow(left, right)
        except OverflowError as exc:
            raise EvalError("Численное переполнение") from exc
        except ValueError as exc:
            raise EvalError("Некорректная операция степени") from exc
        return _ensure_finite(result)

    raise EvalError(f"Неподдерживаемая операция '{node.op}'")
