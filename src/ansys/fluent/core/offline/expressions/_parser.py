# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Parser: Fluent expression string -> :class:`~._ast.Expr` tree.

A small hand-written recursive-descent parser.  Its purpose is
round-tripping and editing: given an existing Fluent expression string
(typed by a user, produced by the GUI, or read back from the server),
produce an :class:`Expr` tree that:

* renders back to an equivalent Fluent expression (canonical form), and
* can be further composed / edited using the builder API.

Supported grammar
-----------------

::

    expr    := compare
    compare := add (('<'|'<='|'>'|'>='|'=='|'!=') add)?
    add     := mul (('+'|'-') mul)*
    mul     := unary (('*'|'/') unary)*
    unary   := ('-'|'+') unary | power
    power   := atom ('**' unary)?
    atom    := NUMBER '[' units ']'          # Quantity
             | NUMBER
             | STRING
             | '[' str_list? ']'             # LocationList
             | IDENT ('.' IDENT)* ('(' args? ')')?
             | '(' expr ')'
    args    := arg (',' arg)*
    arg     := IDENT '=' expr                # KeywordArg
             | expr

Unresolved bare identifiers become :class:`~._ast.RawName` nodes so that
enum-style tokens (``Weight=Area``) and named expressions round-trip
without special-casing.

Not (yet) supported: ``&&`` / ``||`` / ``!`` logical operators.
"""

from __future__ import annotations

from dataclasses import dataclass
import re

from ._ast import (
    _NAMING,
    BinOp,
    Call,
    Compare,
    Expr,
    KeywordArg,
    Kind,
    Literal,
    LocationList,
    Quantity,
    RawName,
    UnaryOp,
    Variable,
)
from ._registry import REGISTRY, Signature
from .errors import ExpressionBuildError

# ---------------------------------------------------------------------------
# Reverse lookup tables (built once at import time)                           #
# --------------------------------------------------------------------------- #


def _build_variable_reverse_map() -> dict[str, object]:
    """Map Fluent expression name (``"AbsolutePressure"``) -> descriptor."""
    mapping = getattr(_NAMING, "_mapping", {})
    return {v: k for k, v in mapping.items()}


def _build_signature_reverse_map() -> dict[str, Signature]:
    """Map Fluent-side function name (``"AreaAve"``) -> :class:`Signature`."""
    out: dict[str, Signature] = {}
    for group in REGISTRY.groups():
        for sig in REGISTRY.group(group).values():
            out[sig.name] = sig
    return out


_VARIABLE_BY_NAME = _build_variable_reverse_map()
_SIGNATURE_BY_NAME = _build_signature_reverse_map()


# --------------------------------------------------------------------------- #
# Tokenizer                                                                   #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class _Token:
    kind: str
    value: str
    start: int
    end: int


_TOKEN_SPEC = [
    ("NUMBER", r"\d+(?:\.\d*)?(?:[eE][+-]?\d+)?|\.\d+(?:[eE][+-]?\d+)?"),
    ("STRING", r"'(?:[^'\\]|\\.)*'"),
    ("IDENT", r"[A-Za-z_][A-Za-z_0-9]*"),
    ("OP", r"\*\*|<=|>=|==|!=|&&|\|\||[+\-*/<>=!^]"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("LBRACK", r"\["),
    ("RBRACK", r"\]"),
    ("COMMA", r","),
    ("DOT", r"\."),
    ("WS", r"[ \t\r\n]+"),
]
_MASTER_RE = re.compile("|".join(f"(?P<{k}>{p})" for k, p in _TOKEN_SPEC))


def _tokenize(text: str) -> list[_Token]:
    tokens: list[_Token] = []
    pos = 0
    for m in _MASTER_RE.finditer(text):
        if m.start() != pos:
            raise ExpressionBuildError(
                f"Unexpected character at position {pos}: {text[pos]!r}"
            )
        kind = m.lastgroup or ""
        pos = m.end()
        if kind == "WS":
            continue
        tokens.append(_Token(kind, m.group(), m.start(), m.end()))
    if pos != len(text):
        raise ExpressionBuildError(
            f"Unexpected character at position {pos}: {text[pos]!r}"
        )
    return tokens


# --------------------------------------------------------------------------- #
# Parser                                                                      #
# --------------------------------------------------------------------------- #


class _Parser:
    def __init__(self, text: str):
        self._text = text
        self._tokens = _tokenize(text)
        self._i = 0

    # ---- token helpers -------------------------------------------------- #

    def _peek(self, offset: int = 0) -> _Token | None:
        idx = self._i + offset
        return self._tokens[idx] if idx < len(self._tokens) else None

    def _eat(self, kind: str, value: str | None = None) -> _Token:
        tok = self._peek()
        if (
            tok is None
            or tok.kind != kind
            or (value is not None and tok.value != value)
        ):
            expected = f"{kind}({value!r})" if value else kind
            got = f"{tok.kind}({tok.value!r})" if tok else "end-of-input"
            raise ExpressionBuildError(f"Expected {expected}, got {got}.")
        self._i += 1
        return tok

    def _match(self, kind: str, value: str | None = None) -> _Token | None:
        tok = self._peek()
        if tok and tok.kind == kind and (value is None or tok.value == value):
            self._i += 1
            return tok
        return None

    # ---- entry point ---------------------------------------------------- #

    def parse(self) -> Expr:
        """Parse the token stream and return the root expression node.

        Raises
        ------
        ExpressionBuildError
            If there are unexpected tokens after the end of the expression.
        """
        expr = self._parse_compare()
        if self._i != len(self._tokens):
            tok = self._peek()
            raise ExpressionBuildError(
                f"Unexpected token {tok.value!r} at position {tok.start}."
            )
        return expr

    # ---- grammar rules -------------------------------------------------- #

    _COMPARE_OPS = {"<", "<=", ">", ">=", "==", "!="}

    def _parse_compare(self) -> Expr:
        left = self._parse_add()
        tok = self._peek()
        if tok and tok.kind == "OP" and tok.value in self._COMPARE_OPS:
            self._i += 1
            right = self._parse_add()
            return Compare(tok.value, left, right)
        return left

    def _parse_add(self) -> Expr:
        left = self._parse_mul()
        while True:
            tok = self._peek()
            if tok and tok.kind == "OP" and tok.value in ("+", "-"):
                self._i += 1
                right = self._parse_mul()
                left = BinOp(tok.value, left, right)
            else:
                return left

    def _parse_mul(self) -> Expr:
        left = self._parse_unary()
        while True:
            tok = self._peek()
            if tok and tok.kind == "OP" and tok.value in ("*", "/"):
                self._i += 1
                right = self._parse_unary()
                left = BinOp(tok.value, left, right)
            else:
                return left

    def _parse_unary(self) -> Expr:
        tok = self._peek()
        if tok and tok.kind == "OP" and tok.value in ("+", "-"):
            self._i += 1
            operand = self._parse_unary()
            if tok.value == "-":
                return UnaryOp("-", operand)
            return operand  # unary + is a no-op
        return self._parse_power()

    def _parse_power(self) -> Expr:
        base = self._parse_atom()
        tok = self._peek()
        if tok and tok.kind == "OP" and tok.value == "**":
            self._i += 1
            exp = self._parse_unary()  # right-associative
            return BinOp("**", base, exp)
        return base

    def _parse_atom(self) -> Expr:
        tok = self._peek()
        if tok is None:
            raise ExpressionBuildError("Unexpected end of input.")

        # Parenthesised sub-expression
        if tok.kind == "LPAREN":
            self._i += 1
            inner = self._parse_compare()
            self._eat("RPAREN")
            return inner

        # Bracketed: either a LocationList or a units suffix (handled with NUMBER).
        if tok.kind == "LBRACK":
            return self._parse_location_list()

        # Number, possibly followed by [units] to form a Quantity
        if tok.kind == "NUMBER":
            self._i += 1
            value = (
                float(tok.value)
                if any(c in tok.value for c in ".eE")
                else int(tok.value)
            )
            nxt = self._peek()
            if nxt and nxt.kind == "LBRACK":
                units = self._parse_units_suffix()
                return Quantity(float(value), units)
            return Literal(value)

        # Bare string literal (rare outside location lists).
        if tok.kind == "STRING":
            self._i += 1
            return RawName(tok.value)

        # Identifier chain, optionally followed by call syntax.
        if tok.kind == "IDENT":
            return self._parse_ident_or_call()

        raise ExpressionBuildError(
            f"Unexpected token {tok.value!r} at position {tok.start}."
        )

    # ---- specific atoms ------------------------------------------------- #

    def _parse_location_list(self) -> LocationList:
        self._eat("LBRACK")
        names: list[str] = []
        if not self._match("RBRACK"):
            while True:
                tok = self._eat("STRING")
                # Strip the single quotes.
                names.append(tok.value[1:-1])
                if not self._match("COMMA"):
                    break
            self._eat("RBRACK")
        return LocationList(tuple(names))

    def _parse_units_suffix(self) -> str:
        """Consume ``[..anything..]`` and return the raw units string.

        Uses source positions so we don't need to model unit tokens.
        """
        lb = self._eat("LBRACK")
        depth = 1
        end_pos = lb.end
        while depth > 0:
            tok = self._peek()
            if tok is None:
                raise ExpressionBuildError("Unterminated units suffix.")
            self._i += 1
            end_pos = tok.end
            if tok.kind == "LBRACK":
                depth += 1
            elif tok.kind == "RBRACK":
                depth -= 1
        # Everything between the opening and closing brackets in the source.
        return self._text[lb.end : end_pos - 1].strip()

    def _parse_ident_or_call(self) -> Expr:
        parts = [self._eat("IDENT").value]
        while self._match("DOT"):
            parts.append(self._eat("IDENT").value)
        name = ".".join(parts)

        # Function call?
        if self._peek() and self._peek().kind == "LPAREN":
            return self._parse_call(name)

        # Bare identifier: try Variable, else RawName (enum tokens etc.).
        descriptor = _VARIABLE_BY_NAME.get(name)
        if descriptor is not None:
            return Variable(descriptor)
        return RawName(name)

    def _parse_call(self, name: str) -> Call:
        self._eat("LPAREN")
        args: list[Expr] = []
        if not self._match("RPAREN"):
            while True:
                args.append(self._parse_arg())
                if not self._match("COMMA"):
                    break
            self._eat("RPAREN")

        sig = _SIGNATURE_BY_NAME.get(name)
        return_kind = sig.returns if sig else Kind.SCALAR
        return Call(name, tuple(args), return_kind=return_kind)

    def _parse_arg(self) -> Expr:
        # Detect ``IDENT '=' expr`` -> KeywordArg without consuming state on failure.
        tok = self._peek()
        nxt = self._peek(1)
        if (
            tok
            and tok.kind == "IDENT"
            and nxt
            and nxt.kind == "OP"
            and nxt.value == "="
        ):
            self._i += 2  # consume IDENT and '='
            value = self._parse_compare()
            return KeywordArg(tok.value, value)
        return self._parse_compare()


# --------------------------------------------------------------------------- #
# Public entry point                                                          #
# --------------------------------------------------------------------------- #


def parse(text: str) -> Expr:
    """Parse a Fluent expression string into an :class:`Expr` tree.

    Raises
    ------
    ExpressionBuildError
        On any lexical or grammatical error.
    """
    if not isinstance(text, str):
        raise ExpressionBuildError(
            f"parse() expects a string, got {type(text).__name__}."
        )
    if not text.strip():
        raise ExpressionBuildError("parse() got an empty string.")
    return _Parser(text).parse()
