"""Calculator package for staged CLI app."""

from .api import calculate, format_number
from .errors import EvalError, ParseError

__all__ = ["calculate", "format_number", "ParseError", "EvalError"]
