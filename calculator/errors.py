class CalcError(Exception):
    """Base calculator error."""


class ParseError(CalcError):
    """Raised when expression cannot be parsed."""


class EvalError(CalcError):
    """Raised when parsed expression cannot be evaluated."""
