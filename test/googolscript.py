import sys
from dataclasses import dataclass
from tokens import T, keyword_map, ignores_newline
from rules import NT
from grammar import grammar
from regexes import token_regex

def parse_table():
    table: dict[tuple[NT, T], set[tuple[T | NT, ...]]] = {(nt, t) : set() for nt in NT for t in T}
    while True:
        modified = False
        for nt, t in table:
            for seq in grammar[nt]:
                if seq not in table[nt, t] and (seq[0] is t or type(seq[0]) is NT and table[seq[0], t]):
                    table[nt, t].add(seq)
                    modified = True
        if not modified: return table

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

def run(source: str) -> bool:
    pt = parse_table()
    tokens = normalize_terminators(tokenize(source))
    print(pt, tokens)
    return True

def repl_intro():
    print("Welcome to the GoogolScript 0.0.2 REPL.")
    print("Commands here will be interpreted the same way as commands from a .gs source file.")
    print("The current exiting keyword is 'EXIT'. For a full grammar specification, see the source code.")
    print("To run code from a .gs source file, you can simply drag-and-drop it onto this script.")

def main():
    match len(sys.argv):
        case 1:
            repl_intro()
            while run(input("> ")): pass
        case 2:
            with open(sys.argv[1], "r", encoding = "utf-8") as file: run(file.read())
        case _: raise Exception("Unexpected number of arguments")

if __name__ == "__main__": main()