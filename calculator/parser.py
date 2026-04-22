import math

from .ast_nodes import BinaryOpNode, FunctionCallNode, NumberNode
from .errors import ParseError
from .lexer import Token, tokenize


CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}


class Parser:
    def __init__(self, tokens: list[Token]):
        self._tokens = tokens
        self._index = 0

    def parse(self):
        node = self._expression()
        current = self._current()
        if current.kind != "EOF":
            raise ParseError(f"Лишний токен '{current.lexeme}' в позиции {current.pos}")
        return node

    def _expression(self):
        node = self._term()
        while self._current().kind in ("PLUS", "MINUS"):
            op_token = self._advance()
            right = self._term()
            node = BinaryOpNode(op_token.lexeme, node, right)
        return node

    def _term(self):
        node = self._unary()
        while self._current().kind in ("MUL", "DIV"):
            op_token = self._advance()
            right = self._unary()
            node = BinaryOpNode(op_token.lexeme, node, right)
        return node

    def _unary(self):
        token = self._current()
        if token.kind == "PLUS":
            self._advance()
            return self._unary()
        if token.kind == "MINUS":
            self._advance()
            return BinaryOpNode("-", NumberNode(0.0), self._unary())
        return self._power()

    def _power(self):
        node = self._primary()
        if self._current().kind == "POW":
            op_token = self._advance()
            right = self._power()
            node = BinaryOpNode(op_token.lexeme, node, right)
        return node

    def _primary(self):
        token = self._current()

        if token.kind == "NUMBER":
            self._advance()
            try:
                return NumberNode(float(token.lexeme))
            except ValueError as exc:
                raise ParseError(f"Некорректное число '{token.lexeme}'") from exc

        if token.kind == "IDENT":
            self._advance()
            name = token.lexeme.lower()

            if self._current().kind == "LPAREN":
                self._advance()
                argument = self._expression()
                if self._current().kind != "RPAREN":
                    raise ParseError(f"Ожидалась ')' в позиции {self._current().pos}")
                self._advance()
                return FunctionCallNode(name, argument)

            if name in CONSTANTS:
                return NumberNode(CONSTANTS[name])

            raise ParseError(f"Неизвестный идентификатор '{token.lexeme}' в позиции {token.pos}")

        if token.kind == "LPAREN":
            self._advance()
            inner = self._expression()
            if self._current().kind != "RPAREN":
                raise ParseError(f"Ожидалась ')' в позиции {self._current().pos}")
            self._advance()
            return inner

        raise ParseError(f"Ожидалось число, идентификатор или '(' в позиции {token.pos}")

    def _current(self) -> Token:
        return self._tokens[self._index]

    def _advance(self) -> Token:
        token = self._tokens[self._index]
        self._index += 1
        return token


def parse(expression: str):
    if expression is None or expression.strip() == "":
        raise ParseError("Пустое выражение")
    parser = Parser(tokenize(expression))
    return parser.parse()
