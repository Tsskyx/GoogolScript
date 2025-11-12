from tokens import T
from rules import NT

# class for sequences of symbols
class Seq:
    def __init__(self, *seq: "T | NT"): self.seq = list(seq)
    def __repr__(self): return str(vars(self))
    def __and__(self, other: "T | NT | Seq"):
        match other:
            case T() | NT(): return Seq(* self.seq + [other])
            case Seq(): return Seq(* self.seq + other.seq)
    def __or__(self, other: "T | NT | Seq"):
        match other:
            case T() | NT(): return Alt(self, Seq(other))
            case Seq(): return Alt(self, other)
    def __rand__(self, other: "T | NT"): return Seq(* [other] + self.seq)
    def __ror__(self, other: "T | NT"): return Alt(Seq(other), self)

# class for alternations of sequences of symbols
class Alt:
    def __init__(self, *alt: Seq): self.alt = list(alt)
    def __repr__(self): return str(vars(self))
    def __and__(self, other: "T | NT | Seq | Alt"):
        match other:
            case T() | NT(): return Alt(* [Seq(* dis.seq + [other]) for dis in self.alt])
            case Seq(): return Alt(* [Seq(* dis.seq + other.seq) for dis in self.alt])
            case Alt(): return Alt(* [Seq(* left.seq + right.seq) for left in self.alt for right in other.alt])
    def __or__(self, other: "T | NT | Seq | Alt"):
        match other:
            case T() | NT(): return Alt(* self.alt + [Seq(other)])
            case Seq(): return Alt(* self.alt + [other])
            case Alt(): return Alt(* self.alt + other.alt)
    def __rand__(self, other: "T | NT | Seq"):
        match other:
            case T() | NT(): return Alt(* [Seq(* [other] + dis.seq) for dis in self.alt])
            case Seq(): return Alt(* [Seq(* other.seq + dis.seq) for dis in self.alt])
    def __ror__(self, other: "T | NT | Seq"):
        match other:
            case T() | NT(): return Alt(* [Seq(other)] + self.alt)
            case Seq(): return Alt(* [other] + self.alt)