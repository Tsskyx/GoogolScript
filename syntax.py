from __future__ import annotations
from dataclasses import dataclass


class Node:
    __match_args__ = ()

    def __repr__(self):
        items = (getattr(self, name) for name in type(self).__match_args__)
        return f"{type(self).__name__}({', '.join(map(repr, items))})"


class Program(Node):
    pass


@dataclass(slots=True, repr=False, init=False)
class Top(Program):
    def __init__(self, *items: Cmd | Label):
        self.items = items

    def __iter__(self):
        return iter(self.items)


class Mode(Node):
    pass


@dataclass(slots=True, repr=False)
class IMM(Mode):
    pass


@dataclass(slots=True, repr=False)
class REG(Mode):
    pass


class Op(Node):
    pass


@dataclass(slots=True, repr=False)
class ADD(Op):
    pass


@dataclass(slots=True, repr=False)
class SUB(Op):
    pass


@dataclass(slots=True, repr=False)
class MUL(Op):
    pass


@dataclass(slots=True, repr=False)
class DIV(Op):
    pass


@dataclass(slots=True, repr=False)
class MOD(Op):
    pass


class Rel(Node):
    pass


@dataclass(slots=True, repr=False)
class EQ(Rel):
    pass


@dataclass(slots=True, repr=False)
class NE(Rel):
    pass


@dataclass(slots=True, repr=False)
class LT(Rel):
    pass


@dataclass(slots=True, repr=False)
class LE(Rel):
    pass


@dataclass(slots=True, repr=False)
class GT(Rel):
    pass


@dataclass(slots=True, repr=False)
class GE(Rel):
    pass


class Label(Node):
    pass


@dataclass(slots=True, repr=False)
class LABEL(Label):
    _0: str


class Cmd(Node):
    pass


@dataclass(slots=True, repr=False)
class MOV(Cmd):
    _0: Mode
    _1: int
    _2: int


@dataclass(slots=True, repr=False)
class LOAD(Cmd):
    _0: int
    _1: int


@dataclass(slots=True, repr=False)
class STORE(Cmd):
    _0: int
    _1: int


@dataclass(slots=True, repr=False)
class OP(Cmd):
    _0: Op
    _1: Mode
    _2: int
    _3: int
    _4: int


@dataclass(slots=True, repr=False)
class JMP(Cmd):
    _0: str


@dataclass(slots=True, repr=False)
class JIF(Cmd):
    _0: Rel
    _1: Mode
    _2: int
    _3: int
    _4: str


@dataclass(slots=True, repr=False)
class READ(Cmd):
    _0: int


@dataclass(slots=True, repr=False)
class WRITE(Cmd):
    _0: int
