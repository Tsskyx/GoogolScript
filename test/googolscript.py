import sys, re
from dataclasses import dataclass
from enum import Enum, auto
from typing import TypeVar
Symb = TypeVar('Symb')

# class for sequences of symbols
class _Seq:
    def __init__(self, *seq: "T | NT"): self.seq = list(seq)
    def __repr__(self): return str(vars(self))
    def __and__(self, other: "T | NT | _Seq"):
        match other:
            case T() | NT(): return _Seq(* self.seq + [other])
            case _Seq(): return _Seq(* self.seq + other.seq)
    def __or__(self, other: "T | NT | _Seq"):
        match other:
            case T() | NT(): return _Alt(self, _Seq(other))
            case _Seq(): return _Alt(self, other)
    def __rand__(self, other: "T | NT"): return _Seq(* [other] + self.seq)
    def __ror__(self, other: "T | NT"): return _Alt(_Seq(other), self)

# class for an alternation of sequences of symbols
class _Alt:
    def __init__(self, *alt: _Seq): self.alt = list(alt)
    def __repr__(self): return str(vars(self))
    def __and__(self, other: "T | NT | _Seq | _Alt"):
        match other:
            case T() | NT(): return _Alt(* [_Seq(* dis.seq + [other]) for dis in self.alt])
            case _Seq(): return _Alt(* [_Seq(* dis.seq + other.seq) for dis in self.alt])
            case _Alt(): return _Alt(* [_Seq(* left.seq + right.seq) for left in self.alt for right in other.alt])
    def __or__(self, other: "T | NT | _Seq | _Alt"):
        match other:
            case T() | NT(): return _Alt(* self.alt + [_Seq(other)])
            case _Seq(): return _Alt(* self.alt + [other])
            case _Alt(): return _Alt(* self.alt + other.alt)
    def __rand__(self, other: "T | NT | _Seq"):
        match other:
            case T() | NT(): return _Alt(* [_Seq(* [other] + dis.seq) for dis in self.alt])
            case _Seq(): return _Alt(* [_Seq(* other.seq + dis.seq) for dis in self.alt])
    def __ror__(self, other: "T | NT | _Seq"):
        match other:
            case T() | NT(): return _Alt(* [_Seq(other)] + self.alt)
            case _Seq(): return _Alt(* [other] + self.alt)

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

    def __and__(self, other: "T | NT"): return _Seq(self, other)
    def __or__(self, other: "T | NT"): return _Alt(_Seq(self), _Seq(other))

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

keywords = {
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

# non-terminals
class NT(Enum):
    prog      = auto()
    cmd_sep   = auto()
    cmd       = auto()
    cmd_def   = auto()
    cmd_input = auto()
    cmd_if    = auto()
    cmd_ifel  = auto()
    cmd_while = auto()
    cmd_print = auto()
    cmd_exit  = auto()
    prog_opt  = auto()
    form      = auto()
    form_elem = auto()
    bool_op1  = auto()
    bool_op2  = auto()
    pred      = auto()
    cmp       = auto()
    term      = auto()
    term_one  = auto()
    term_op1  = auto()
    term_op2  = auto()
    lit       = auto()

    def __and__(self, other: "T | NT"): return _Seq(self, other)
    def __or__(self, other: "T | NT"): return _Alt(_Seq(self), _Seq(other))
    def __gt__(self, other: "T | NT | _Seq | _Alt"):
        match other:
            case T() | NT(): return Rule(self, [[other]])
            case _Seq(): return Rule(self, [other.seq])
            case _Alt(): return Rule(self, [alt.seq for alt in other.alt])

@dataclass
class Rule:
    left: NT; right: list[list[T | NT]]
    def __repr__(self): return str(vars(self))

grammar = { rule.left : rule.right for rule in [
    NT.prog      > NT.cmd | NT.cmd & NT.cmd_sep & NT.prog,
    NT.cmd_sep   > T.SEMI & NT.cmd_sep,
    NT.cmd       > NT.cmd_def | NT.cmd_if | NT.cmd_ifel | NT.cmd_while | NT.cmd_print | NT.cmd_input | NT.cmd_exit,
    NT.cmd_def   > T.LABEL & T.WALRUS & NT.term,
    NT.cmd_input > T.LABEL & T.WALRUS & T.INPUT,
    NT.cmd_if    > T.IF & NT.form & T.THEN & NT.prog_opt & T.END,
    NT.cmd_ifel  > T.IF & NT.form & T.THEN & NT.prog_opt & T.ELSE & NT.prog_opt & T.END,
    NT.cmd_while > T.WHILE & NT.form & T.THEN & NT.prog_opt & T.END,
    NT.cmd_print > T.PRINT & NT.term,
    NT.cmd_exit  > T.EXIT,
    NT.prog_opt  > NT.prog | T.SKIP,
    NT.form      > NT.form_elem | NT.form_elem & NT.bool_op2 & NT.form,
    NT.form_elem > NT.pred | NT.bool_op1 & NT.form_elem | T.LPAREN & NT.form & T.RPAREN,
    NT.bool_op1  > T.NOT,
    NT.bool_op2  > T.AND | T.OR | T.IMPL | T.EQUIV,
    NT.pred      > NT.term & NT.cmp & NT.term | NT.term & NT.cmp & NT.pred,
    NT.cmp       > T.EQ | T.NE | T.LT | T.LE | T.GT | T.GE,
    NT.term      > NT.term_one | NT.term_one & NT.term_op2 & NT.term,
    NT.term_one  > NT.lit | NT.term_op1 & NT.term_one | T.LPAREN & NT.term & T.RPAREN,
    NT.term_op1  > T.MINUS,
    NT.term_op2  > T.PLUS | T.MINUS | T.TIMES | T.DIV | T.MOD,
    NT.lit       > T.INT | T.LABEL,
]}

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
            if token.type is T.LABEL and (word := token.text) in keywords:
                token.type = keywords[word]
            tokens.append(token)
        pos += token.length
        col = 1 if token.type is T.NEWLINE else col + token.length
        line += token.type is T.NEWLINE
    return tokens + [Token(T.EOF)]

def parse(tokens: list[Token]):
    tokens = normalize_terminators(tokens)
    FIRST = calc_first()
    FOLLOW = calc_follow(FIRST)
    print(FOLLOW)

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

def try_add(what: Symb, where: set[Symb]):
    if what in where: return False
    where.add(what); return True

def calc_first():
    FIRST: dict[NT, set[T]] = {rule: set() for rule in grammar}
    while True:
        modified = False
        for key in grammar:
            for prod in grammar[key]:
                match first := prod[0]:
                    case T():
                        modified |= try_add(first, FIRST[key])
                    case NT():
                        for t in FIRST[first]:
                            modified |= try_add(t, FIRST[key])
        if not modified: return FIRST

def calc_follow(FIRST: dict[NT, set[T]]):
    FOLLOW: dict[NT, set[T]] = {rule: set() for rule in grammar}
    FOLLOW[list(grammar)[0]].add(T.EOF)
    while True:
        modified = False
        for key in grammar:
            for prod in grammar[key]:
                for i in range(len(prod)-1):
                    s1, s2 = prod[i], prod[i+1]
                    if type(s1) is not NT: continue
                    match s2:
                        case T():
                            modified |= try_add(s2, FOLLOW[s1])
                        case NT():
                            for t in FIRST[s2]:
                                modified |= try_add(t, FOLLOW[s1])
                if type(s := prod[-1]) is not NT: continue
                for t in FOLLOW[key]:
                    modified |= try_add(t, FOLLOW[s])
        if not modified: return FOLLOW



"""
def parse_table(grammar: dict[NT, list[list[T | NT]]], FIRST: dict[NT, set[T]]):
    table: dict[tuple[NT, T], list[T | NT]] = {}
    conflicts: list[tuple[NT, T, list[T | NT], list[T | NT]]] = []
    for key in grammar:
        for prod in grammar[key]:
            first = prod[0]
            match first:
                case T(): firsts = {first}
                case NT(): firsts = FIRST[first]
            for a in firsts:
                key = (key, a)
                prev = table.get(key)
                if prev is None:
                    table[key] = prod
                elif prev != prod:
                    conflicts.append((key, a, prev, prod))
    return table, conflicts
"""



def main():
    match len(sys.argv):
        case 1:
            repl()
        case 2:
            with open(sys.argv[1], "r", encoding = "utf-8") as file:
                source = file.read()
            if not source: return
            tokens = tokenize(source)
            AST = parse(tokens)
            print(AST)
        case _:
            raise Exception("Unexpected number of arguments")

def repl():
    print("Welcome to the GoogolScript 0.0.2 REPL.")
    print("Commands here will be interpreted the same way as commands from a .gs source file.")
    print("The current exiting keyword is 'EXIT'. For a full grammar specification, see the source code.")
    print("To run code from a .gs source file, you can simply drag-and-drop it onto this script.")
    while True:
        try:
            tokens = tokenize(input("> "))
            AST = parse(tokens)
            print(AST)
        except Exception as e:
            print(str(e))

if __name__ == "__main__":
    main()

r"""

left := 0
right := 1
sum := 0
n := INPUT
WHILE n > 0 THEN
    sum := left + right
    left := right
    right := sum
    n := n - 1
END
PRINT sum

left := 0 ; right := 1 ; sum := 0 ; n := INPUT ; WHILE n >= 0 THEN sum := left + right ; left := right ; right := sum ; n := n - 1 ; END PRINT sum

"""








