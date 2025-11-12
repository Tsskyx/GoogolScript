from enum import Enum, auto
from tokens import T
from grammar_syntax import Seq, Alt
from grammar import Rule

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

    def __and__(self, other: "T | NT"): return Seq(self, other)
    def __or__(self, other: "T | NT"): return Alt(Seq(self), Seq(other))
    def __gt__(self, other: "T | NT | Seq | Alt"):
        match other:
            case T() | NT(): return Rule(self, [tuple([other])])
            case Seq(): return Rule(self, [tuple(other.seq)])
            case Alt(): return Rule(self, [tuple(alt.seq) for alt in other.alt])