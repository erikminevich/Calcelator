from dataclasses import dataclass


@dataclass(frozen=True)
class NumberNode:
    value: float


@dataclass(frozen=True)
class BinaryOpNode:
    op: str
    left: object
    right: object
