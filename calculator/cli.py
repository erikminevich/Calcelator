import argparse
import sys

from .api import calculate, format_number
from .errors import EvalError, ParseError


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="calc", description="CLI calculator")
    parser.add_argument(
        "--angle-unit",
        choices=["radian", "degree"],
        default="radian",
        help="Angle unit for trigonometric functions",
    )
    parser.add_argument("expression", help="Arithmetic expression")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    try:
        result = calculate(args.expression, angle_unit=args.angle_unit)
        print(format_number(result))
        return 0
    except ParseError as exc:
        print(f"Ошибка парсера: {exc}", file=sys.stderr)
        return 1
    except EvalError as exc:
        print(f"Ошибка при вычислении: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
