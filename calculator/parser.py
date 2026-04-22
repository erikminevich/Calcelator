from .ast_nodes import BinaryOpNode, NumberNode
from .errors import ParseError
from .lexer import Token, tokenize


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
        node = self._factor()
        while self._current().kind in ("MUL", "DIV"):
            op_token = self._advance()
            right = self._factor()
            node = BinaryOpNode(op_token.lexeme, node, right)
        return node

    def _factor(self):
        token = self._current()
        if token.kind == "NUMBER":
            self._advance()
            try:
                return NumberNode(float(token.lexeme))
            except ValueError as exc:
                raise ParseError(f"Некорректное число '{token.lexeme}'") from exc

        raise ParseError(f"Ожидалось число в позиции {token.pos}")

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
