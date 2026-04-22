from dataclasses import dataclass

from .errors import ParseError


@dataclass(frozen=True)
class Token:
    kind: str
    lexeme: str
    pos: int


def tokenize(text: str) -> list[Token]:
    tokens: list[Token] = []
    i = 0
    length = len(text)

    while i < length:
        ch = text[i]

        if ch.isspace():
            i += 1
            continue

        if ch.isdigit() or ch == ".":
            start = i
            has_digits = False

            while i < length and text[i].isdigit():
                has_digits = True
                i += 1

            if i < length and text[i] == ".":
                i += 1
                while i < length and text[i].isdigit():
                    has_digits = True
                    i += 1

            if not has_digits:
                raise ParseError(f"Некорректное число в позиции {start}")

            if i < length and text[i] in ("e", "E"):
                i += 1
                if i < length and text[i] in ("+", "-"):
                    i += 1

                exp_start = i
                while i < length and text[i].isdigit():
                    i += 1

                if exp_start == i:
                    raise ParseError(f"Некорректная экспонента в позиции {start}")

            tokens.append(Token("NUMBER", text[start:i], start))
            continue

        if ch == "+":
            tokens.append(Token("PLUS", ch, i))
            i += 1
            continue
        if ch == "-":
            tokens.append(Token("MINUS", ch, i))
            i += 1
            continue
        if ch == "*":
            tokens.append(Token("MUL", ch, i))
            i += 1
            continue
        if ch == "/":
            tokens.append(Token("DIV", ch, i))
            i += 1
            continue
        if ch == "^":
            tokens.append(Token("POW", ch, i))
            i += 1
            continue
        if ch == "(":
            tokens.append(Token("LPAREN", ch, i))
            i += 1
            continue
        if ch == ")":
            tokens.append(Token("RPAREN", ch, i))
            i += 1
            continue

        raise ParseError(f"Неподдерживаемый символ '{ch}' в позиции {i}")

    tokens.append(Token("EOF", "", length))
    return tokens
