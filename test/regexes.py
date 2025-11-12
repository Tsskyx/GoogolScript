import re
from tokens import T

token_regex = {k : re.compile(v) for k, v in {
    T.NEWLINE : r"\n",
    T.WS      : r"[ \t]+",
    T.LPAREN  : r"\(",
    T.RPAREN  : r"\)",
    T.PLUS    : r"\+",
    T.MINUS   : r"-",
    T.TIMES   : r"\*",
    T.DIV     : r"/",
    T.MOD     : r"%",
    T.EQ      : r"==",
    T.NE      : r"!=",
    T.GT      : r">",
    T.LT      : r"<",
    T.GE      : r">=",
    T.LE      : r"<=",
    T.SEMI    : r";",
    T.WALRUS  : r":=",
    T.INT     : r"[0-9]+",
    T.LABEL   : r"[A-Za-z_][A-Za-z_0-9]*",
}.items()}