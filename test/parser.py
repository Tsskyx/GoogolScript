from tokens import T, NT
from grammar import Grammar, grammar
from enum import Enum, auto

def calc_null():
    class NTS(Enum):
        CAN_NULL = auto()
        NOT_NULL = auto()
        UNSORTED = auto()
    
    nt_state = {L : NTS.UNSORTED for L in grammar}

    # returns NTS.CAN_NULL if the production can be nulled
    # returns NTS.NOT_NULL if the production cannot be nulled
    # returns NTS.UNSORTED if the nullability of the production cannot yet be determined
    def calc_prod(prod: list[T | NT]) -> NTS:
        if not prod: return NTS.CAN_NULL
        for symb in prod:
            match symb:
                case T(): return NTS.NOT_NULL
                case NT():
                    match nt_state[symb]:
                        case NTS.CAN_NULL: continue
                        case NTS.NOT_NULL: return NTS.NOT_NULL
                        case NTS.UNSORTED: return NTS.UNSORTED
        return NTS.CAN_NULL
    
    # returns True/False based on if nt_state changed
    def calc_rule(L: NT):
        for prod in grammar[L]:
            match calc_prod(prod):
                case NTS.CAN_NULL:
                    nt_state[L] = NTS.CAN_NULL
                    return True
                case NTS.NOT_NULL:
                    continue
                case NTS.UNSORTED:
                    return False
        nt_state[L] = NTS.NOT_NULL
        return True

    # loops as long as nt_state keeps changing, then returns the nullable non-terminals
    def calc():
        while True:
            changed = False
            for L in reversed(grammar):
                if nt_state[L] is NTS.UNSORTED and calc_rule(L):
                    changed = True
            if not changed: break
        return {L for L in grammar if nt_state[L] is NTS.CAN_NULL}

    return calc()

def calc_first() -> dict[NT, set[T]]:
    FIRST: dict[NT, set[T]] = {nt: set() for nt in NT}
    while True:
        changed = False
        for L, R in reversed(grammar.items()):
            for prod in R:
                if not prod: continue
                match s0 := prod[0]:
                    case T():
                        if s0 not in FIRST[L]:
                            FIRST[L].add(s0)
                            changed = True
                    case NT():
                        for t in FIRST[s0]:
                            if t not in FIRST[L]:
                                FIRST[L].add(t)
                                changed = True
        if not changed: return FIRST

def calc_follow(FIRST: dict[NT, set[T]], NULLABLE: set[NT]) -> dict[NT, set[T]]:
    FOLLOW: dict[NT, set[T]] = {nt: set() for nt in NT}
    FOLLOW[list(grammar)[0]].add(T.EOF)

    while True:
        changed = False
        for L, R in reversed(grammar.items()):
            for prod in R:
                for i in range(len(prod)-1):
                    if type(prod[i]) is not NT: continue
                    for j in range(i+1, len(prod)):
                        next = prod[j+1]
                        match next:
                            case T():
                                FOLLOW[L].add(next)
                                changed = True
                            case NT():
                                for t in FIRST[next]:
                                    FOLLOW[L].add(t)
                                    changed = True
        if not changed: return FOLLOW
















type Table = dict[tuple[NT, T], set[tuple[T | NT, ...]]]

def table(grammar: Grammar):
    pass

class AST:
    pass

def parse(source: str):
    return AST()