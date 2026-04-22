import math

from .ast_nodes import BinaryOpNode, FunctionCallNode, NumberNode
from .errors import EvalError


VALID_ANGLE_UNITS = {"radian", "degree"}


def _ensure_finite(value: float) -> float:
    if not math.isfinite(value):
        raise EvalError("Численное переполнение")
    return value


def _to_radian(value: float, angle_unit: str) -> float:
    if angle_unit == "degree":
        return math.radians(value)
    return value


def _evaluate_function(name: str, arg: float, angle_unit: str) -> float:
    if name == "sqrt":
        if arg < 0.0:
            raise EvalError("sqrt от отрицательного значения")
        return math.sqrt(arg)

    if name == "sin":
        return math.sin(_to_radian(arg, angle_unit))

    if name == "cos":
        return math.cos(_to_radian(arg, angle_unit))

    if name in {"tg", "tan"}:
        return math.tan(_to_radian(arg, angle_unit))

    if name == "ctg":
        tangent = math.tan(_to_radian(arg, angle_unit))
        if abs(tangent) < 1e-15:
            raise EvalError("Деление на ноль в ctg")
        return 1.0 / tangent

    if name == "ln":
        if arg <= 0.0:
            raise EvalError("ln определен только для положительных значений")
        return math.log(arg)

    if name == "exp":
        try:
            return math.exp(arg)
        except OverflowError as exc:
            raise EvalError("Численное переполнение") from exc

    raise EvalError(f"Неподдерживаемая функция '{name}'")


def evaluate(node, angle_unit: str = "radian") -> float:
    if angle_unit not in VALID_ANGLE_UNITS:
        raise EvalError(f"Неподдерживаемая единица угла '{angle_unit}'")

    if isinstance(node, NumberNode):
        return _ensure_finite(node.value)

    if isinstance(node, FunctionCallNode):
        argument = evaluate(node.argument, angle_unit=angle_unit)
        return _ensure_finite(_evaluate_function(node.name, argument, angle_unit))

    if not isinstance(node, BinaryOpNode):
        raise EvalError("Неизвестный узел выражения")

    left = evaluate(node.left, angle_unit=angle_unit)
    right = evaluate(node.right, angle_unit=angle_unit)

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
