from enum import Enum, auto
from rules import NT
from grammar_syntax import Seq, Alt

# token types
class T(Enum):
    NEWLINE = auto()
    WS      = auto()
    LPAREN  = auto()
    RPAREN  = auto()
    PLUS    = auto()
    MINUS   = auto()
    TIMES   = auto()
    DIV     = auto()
    MOD     = auto()
    EQ      = auto()
    NE      = auto()
    GT      = auto()
    LT      = auto()
    GE      = auto()
    LE      = auto()
    SEMI    = auto()
    WALRUS  = auto()
    INT     = auto()
    LABEL   = auto()
    NOT     = auto()
    AND     = auto()
    OR      = auto()
    IMPL    = auto()
    EQUIV   = auto()
    IF      = auto()
    ELSE    = auto()
    WHILE   = auto()
    THEN    = auto()
    END     = auto()
    SKIP    = auto()
    EXIT    = auto()
    PRINT   = auto()
    INPUT   = auto()
    EOF     = auto()

    def __and__(self, other: "T | NT"): return Seq(self, other)
    def __or__(self, other: "T | NT"): return Alt(Seq(self), Seq(other))

keyword_map = {
    "NOT": T.NOT, "AND": T.AND, "OR": T.OR, "IMPL": T.IMPL, "EQUIV": T.EQUIV,
    "IF": T.IF, "ELSE": T.ELSE, "WHILE": T.WHILE, "THEN": T.THEN, "END": T.END, "SKIP": T.SKIP,
    "PRINT": T.PRINT, "INPUT": T.INPUT, "EXIT": T.EXIT,
}

ignores_newline = {
    T.LPAREN,
    T.PLUS, T.MINUS, T.TIMES, T.DIV, T.MOD,
    T.EQ, T.NE, T.GT, T.LT, T.GE, T.LE,
    T.THEN, T.WALRUS,
    T.SEMI
}