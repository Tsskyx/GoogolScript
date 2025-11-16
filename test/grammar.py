from dataclasses import dataclass
from tokens import T, NT

@dataclass
class Symb:
    symb: T | NT
    
    def __and__(self, other: "Symb | Word") -> "Word":
        match other:
            case Symb(): return Word([self, other])
            case Word(): return Word([self] + other.seq)

    def __or__(self, other: "Symb | Word | Alts") -> "Alts":
        match other:
            case Symb(): return Alts([Word([self]), Word([other])])
            case Word(): return Alts([Word([self]), other])
            case Alts(): return Alts([Word([self])] + other.alt)

    def __gt__(self, other: "Symb | Word | Alts") -> "Rule":
        match other:
            case Symb(): return Rule(Word([self]), Alts([Word([other])]))
            case Word(): return Rule(Word([self]), Alts([other]))
            case Alts(): return Rule(Word([self]), other)

@dataclass
class Word:
    seq: list[Symb] = []

    def __and__(self, other: "Symb | Word") -> "Word":
        match other:
            case Symb(): return Word(self.seq + [other])
            case Word(): return Word(self.seq + other.seq)
    
    def __rand__(self, other: "Symb") -> "Word":
        return Word([other] + self.seq)
    
    def __or__(self, other: "Symb | Word") -> "Alts":
        match other:
            case Symb(): return Alts([self, Word([other])])
            case Word(): return Alts([self, other])

    def __ror__(self, other: "Symb") -> "Alts":
        return Alts([Word([other]), self])

    def __gt__(self, other: "Symb | Word | Alts") -> "Rule":
        match other:
            case Symb(): return Rule(self, Alts([Word([other])]))
            case Word(): return Rule(self, Alts([other]))
            case Alts(): return Rule(self, other)

@dataclass
class Alts:
    alt: list[Word]

    def __and__(self, other: "Symb | Word | Alts") -> "Alts":
        match other:
            case Symb(): return Alts([Word(dis.seq + [other]) for dis in self.alt])
            case Word(): return Alts([Word(dis.seq + other.seq) for dis in self.alt])
            case Alts(): return Alts([Word(left.seq + right.seq) for left in self.alt for right in other.alt])
    
    def __rand__(self, other: "Symb | Word") -> "Alts":
        match other:
            case Symb(): return Alts([Word([other] + dis.seq) for dis in self.alt])
            case Word(): return Alts([Word(other.seq + dis.seq) for dis in self.alt])
    
    def __or__(self, other: "Symb | Word | Alts") -> "Alts":
        match other:
            case Symb(): return Alts(self.alt + [Word([other])])
            case Word(): return Alts(self.alt + [other])
            case Alts(): return Alts(self.alt + other.alt)
    
    def __ror__(self, other: "Symb | Word") -> "Alts":
        match other:
            case Symb(): return Alts([Word([other])] + self.alt)
            case Word(): return Alts([other] + self.alt)

@dataclass
class Rule:
    left: Word
    right: Alts

S = Symb
W = Word
A = Alts
R = Rule

rules = [
    S(NT.prog)      > S(NT.cmd) | S(NT.cmd) & S(NT.cmd_sep) & S(NT.prog),
    S(NT.cmd_sep)   > S(T.SEMI) & S(NT.cmd_sep),
    S(NT.cmd)       > S(NT.cmd_def) | S(NT.cmd_if) | S(NT.cmd_ifel) | S(NT.cmd_while) | S(NT.cmd_print) | S(NT.cmd_input) | S(NT.cmd_exit),
    S(NT.cmd_def)   > S(T.LABEL) & S(T.WALRUS) & S(NT.term),
    S(NT.cmd_input) > S(T.LABEL) & S(T.WALRUS) & S(T.INPUT),
    S(NT.cmd_if)    > S(T.IF) & S(NT.form) & S(T.THEN) & S(NT.prog) & S(T.END),
    S(NT.cmd_ifel)  > S(T.IF) & S(NT.form) & S(T.THEN) & S(NT.prog) & S(T.ELSE) & S(NT.prog) & S(T.END),
    S(NT.cmd_while) > S(T.WHILE) & S(NT.form) & S(T.THEN) & S(NT.prog) & S(T.END),
    S(NT.cmd_print) > S(T.PRINT) & S(NT.term),
    S(NT.cmd_exit)  > S(T.EXIT),
    S(NT.form)      > S(NT.form_elem) | S(NT.form_elem) & S(NT.bool_op2) & S(NT.form),
    S(NT.form_elem) > S(NT.pred) | S(NT.bool_op1) & S(NT.form_elem) | S(T.LPAREN) & S(NT.form) & S(T.RPAREN),
    S(NT.bool_op1)  > S(T.NOT),
    S(NT.bool_op2)  > S(T.AND) | S(T.OR) | S(T.IMPL) | S(T.EQUIV),
    S(NT.pred)      > S(NT.term) & S(NT.cmp) & S(NT.term) | S(NT.term) & S(NT.cmp) & S(NT.pred),
    S(NT.cmp)       > S(T.EQ) | S(T.NE) | S(T.LT) | S(T.LE) | S(T.GT) | S(T.GE),
    S(NT.term)      > S(NT.term_one) | S(NT.term_one) & S(NT.term_op2) & S(NT.term),
    S(NT.term_one)  > S(NT.lit) | S(NT.term_op1) & S(NT.term_one) | S(T.LPAREN) & S(NT.term) & S(T.RPAREN),
    S(NT.term_op1)  > S(T.MINUS),
    S(NT.term_op2)  > S(T.PLUS) | S(T.MINUS) | S(T.TIMES) | S(T.DIV) | S(T.MOD),
    S(NT.lit)       > S(T.INT) | S(T.LABEL),
]

type Grammar = dict[NT, tuple[tuple[T | NT, ...], ...]]

grammar: Grammar = dict()

for rule in rules:
    L_seq = rule.left.seq
    if len(L_seq) == 1 and type(L_seq[0].symb) is NT:
        grammar[L_seq[0].symb] = tuple(tuple(seq.symb for seq in alt.seq) for alt in rule.right.alt)
    else:
        raise Exception("Cannot make context-free grammar from the specified rules")

start = NT.prog