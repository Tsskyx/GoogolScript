from tokens import T
from rules import NT, grammar

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

class AST:
    pass

def parse(source: str):
    return AST()