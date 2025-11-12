from dataclasses import dataclass
from tokens import T
from rules import NT

@dataclass
class Rule:
    left: NT; right: list[tuple[T | NT, ...]]
    def __repr__(self): return str(vars(self))

def_grammar: list[Rule] = [
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
]

grammar = { rule.left : rule.right for rule in def_grammar}