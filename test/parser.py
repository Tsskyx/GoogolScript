from tokens import T, NT, tokenize
from grammar import Grammar, grammar, start

def calc_nullable(grammar: Grammar) -> set[NT]:
    nullable: set[NT] = set()
    while True:
        changed = False
        for L, R in grammar.items():
            if L in nullable: continue
            rule_nullable = False
            for prod in R:
                prod_nullable = True
                for symb in prod:
                    if type(symb) is T or symb not in nullable:
                        prod_nullable = False
                        break
                if prod_nullable:
                    rule_nullable = True
                    break
            if rule_nullable:
                nullable.add(L)
                changed = True
        if not changed: return nullable

type SetT = dict[NT, set[T]]
type SetNT = dict[NT, set[NT]]

def calc_first(grammar: Grammar, NULLABLE: set[NT]) -> SetT:
    FIRST: SetT = {nt: set() for nt in grammar.keys()}
    while True:
        changed = False
        for L, R in grammar.items():
            for prod in R:
                for symb in prod:
                    first = {symb} if isinstance(symb, T) else FIRST[symb]
                    if not first.issubset(FIRST[L]): changed = True
                    FIRST[L] |= first
                    if symb not in NULLABLE: break
        if not changed: return FIRST

def calc_follow(grammar: Grammar, start: NT, FIRST: SetT, NULLABLE: set[NT]) -> SetT:
    FOLLOW: SetT = {nt: set() for nt in grammar.keys()}
    FOLLOW[start].add(T.EOF)
    while True:
        changed = False
        for L, R in grammar.items():
            for prod in R:
                for i, symb in enumerate(prod):
                    if isinstance(symb, T): continue
                    follow: set[T] = set()
                    for next in prod[i+1:]:
                        follow |= {next} if isinstance(next, T) else FIRST[next]
                        if isinstance(next, T) or next not in NULLABLE: break
                    else:
                        follow |= FOLLOW[L]
                    if not follow.issubset(FOLLOW[symb]): changed = True
                    FOLLOW[symb] |= follow
        if not changed: return FOLLOW

def check_undefined_NTs(grammar: Grammar) -> set[NT]:
    L_NT = {L for L in grammar.keys()}
    R_NT: set[NT] = {symb for R in grammar.values() for prod in R for symb in prod if type(symb) is NT}
    return R_NT - L_NT

def check_unused_NTs(grammar: Grammar) -> set[NT]:
    L_NT = {L for L in grammar.keys()}
    R_NT: set[NT] = {symb for R in grammar.values() for prod in R for symb in prod if type(symb) is NT}
    return L_NT - R_NT

def check_unreachable_rules(grammar: Grammar, start: NT) -> set[NT]:
    reachable = {start}
    while True:
        changed = False
        for L, R in grammar.items():
            if L not in reachable: continue
            for prod in R:
                for symb in prod:
                    if type(symb) is NT and symb not in reachable:
                        reachable.add(symb)
                        changed = True
        if not changed: return {nt for nt in grammar.keys()} - reachable

def check_nonterminating_rules(grammar: Grammar) -> set[NT]:
    terminating: set[NT] = set()
    while True:
        changed = False
        for L, R in grammar.items():
            if L in terminating: continue
            for prod in R:
                all_terminating = True
                for symb in prod:
                    if type(symb) is NT and symb not in terminating:
                        all_terminating = False
                        break
                if all_terminating:
                    terminating.add(L)
                    changed = True
                    break
        if not changed: return {nt for nt in grammar.keys()} - terminating

type Prod = tuple[T | NT, ...]
type Table = dict[tuple[NT, T], set[Prod]]

def calc_table(grammar: Grammar, FIRST: SetT, FOLLOW: SetT, NULLABLE: set[NT]) -> Table:
    table: Table = {(L, t): set() for L in grammar.keys() for t in T}
    for L, R in grammar.items():
        for prod in R:
            cols: set[T] = set()
            for symb in prod:
                cols |= {symb} if isinstance(symb, T) else FIRST[symb]
                if isinstance(symb, T) or symb not in NULLABLE: break
            else: cols |= FOLLOW[L]
            for t in cols: table[L, t].add(prod)
    return table

def check_table_conflicts(table: Table) -> Table:
    return {(L, t): R for (L, t), R in table.items() if len(R) > 1}

class AST:
    pass

def parse(source: str) -> AST:
    if unused := check_unused_NTs(grammar):
        raise Exception(f"Unused nonterminals: {sorted(nt.name for nt in unused)}")
    if undefined := check_undefined_NTs(grammar):
        raise Exception(f"Undefined nonterminals: {sorted(nt.name for nt in undefined)}")
    if unreachable := check_unreachable_rules(grammar, start):
        raise Exception(f"Unreachable nonterminals: {sorted(nt.name for nt in unreachable)}")
    if nonterminating := check_nonterminating_rules(grammar):
        raise Exception(f"Nonterminating nonterminals: {sorted(nt.name for nt in nonterminating)}")

    NULLABLE = calc_nullable(grammar)
    FIRST = calc_first(grammar, NULLABLE)
    FOLLOW = calc_follow(grammar, start, FIRST, NULLABLE)

    table = calc_table(grammar, FIRST, FOLLOW, NULLABLE)
    if conflicts := check_table_conflicts(table):
        raise Exception("\n".join(
            f"Table[{L.name}, {t.name}] has multiple productions: " + 
            ",".join(" ".join(str(symb) for symb in prod) for prod in R)
            for (L, t), R in conflicts.items()
        ))
    
    tokens = tokenize(source)
    stack: list[T | NT] = [T.EOF, start]
    i = 0; next = tokens[i].type
    while stack:
        match top := stack.pop():
            case T():
                if top is not next:
                    raise Exception(f"Expected {top.name}, got {next.name}")
                if top is T.EOF:
                    if i != len(tokens) - 1: raise Exception("Extra tokens after EOF")
                    return AST()
                i += 1; next = tokens[i].type
            case NT():
                prods = table[top, next]
                if not prods:
                    raise Exception(f"No rule for ({top.name}, {next.name}) in parse table")
                if len(prods) > 1:
                    raise Exception(f"Conflicting productions for ({top.name}, {next.name}): {"\n".join(str(prod) for prod in prods)}")
                for symb in reversed(tuple(prods)[0]):
                    stack.append(symb)
    if next is not T.EOF: raise Exception("Input remaining after stack empty")
    return AST()