from enum import Enum, auto
from rules import NT
from grammar_syntax import Seq, Alt
from dataclasses import dataclass
from regexes import token_regex

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

@dataclass
class Token:
    type: T
    text: str = ""
    length: int = 0
    pos: tuple[int, int] = (0, 0)
    line: tuple[int, int] = (0, 0)
    col: tuple[int, int] = (0, 0)
    def __repr__(self): return str(vars(self))

def tokenize(source: str):
    tokens: list[Token] = []
    pos = 0; line = 0; col = 0
    while pos < len(source):
        token: Token | None = None
        for rank, type in enumerate(token_regex):
            match = token_regex[type].match(source, pos)
            if not match: continue
            end = match.end()
            length = end - pos
            if token is None or length > token.length or length == token.length and rank < list(token_regex).index(token.type):
                text = source[pos : end]
                nc = text.count("\n")
                cc = len(text.split("\n")[-1])
                token = Token(type, text, length, (pos, end), (line, line + nc), (col, cc if nc else col + cc))
        if token is None:
            raise Exception(f"Could not find a match at position ({line}, {col}).")
        if token.length == 0:
            raise Exception(f"Token {token.type} matched empty string at position ({line}, {col}).")
        if token.type is not T.WS:
            if token.type is T.LABEL and (word := token.text) in keyword_map:
                token.type = keyword_map[word]
            tokens.append(token)
        pos += token.length
        col = 1 if token.type is T.NEWLINE else col + token.length
        line += token.type is T.NEWLINE
    return tokens + [Token(T.EOF)]

def normalize_terminators(tokens: list[Token]):
    depth = 0
    prev_token: Token | None = None
    new_tokens: list[Token] = []
    for token in tokens:
        match token.type:
            case T.LPAREN:
                depth += 1
            case T.RPAREN:
                depth -= 1
                if depth < 0: raise Exception(f"Unbalanced brackets at ({token.line[0]}, {token.col[0]})")
            case T.SEMI:
                if prev_token is not None and prev_token.type is T.SEMI: continue
            case T.NEWLINE:
                if depth == 0 and prev_token is not None and prev_token.type not in ignores_newline:
                    token = Token(T.SEMI)
                else:
                    continue
            case _: pass
        new_tokens.append(token)
        prev_token = token
    return new_tokens