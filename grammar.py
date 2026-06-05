"""
from __future__ import annotations


class Node:
    __match_args__ = ("cons", "args")
    
    def __init__(self, cons: str, args: tuple[object, ...]):
        self.cons = cons
        self.args = args
    
    def __repr__(self):
        return f"{type(self).__name__}.{self.cons}({', '.join(map(repr, self.args))})"


class Prog(Node):
    @classmethod
    def prog(cls, *args: Cmd):
        return cls("prog", args)


class Cmd(Node):
    @classmethod
    def print(cls, _0: Expr):
        return cls("print", (_0,))


class Expr(Node):
    @classmethod
    def lit(cls, _0: int):
        return cls("lit", (_0,))

    @classmethod
    def add(cls, *args: Expr):
        return cls("add", args)

    @classmethod
    def sub(cls, _0: Expr, _1: Expr):
        return cls("sub", (_0, _1))

    @classmethod
    def mul(cls, *args: Expr):
        return cls("mul", args)

    @classmethod
    def div(cls, _0: Expr, _1: Expr):
        return cls("div", (_0, _1))

    @classmethod
    def mod(cls, _0: Expr, _1: Expr):
        return cls("mod", (_0, _1))
"""

from __future__ import annotations


class Node:
    __match_args__ = ("args", )
    def __init__(self, args: tuple[object, ...]):
        self.args = args
    def __len__(self):
        return len(self.args)
    def __getitem__(self, key: int):
        return self.args[key]
    def __repr__(self):
        return f"{type(self).__name__}({', '.join(map(repr, self.args))})"


class Root(Node):
    pass
class Prog(Root):
    def __init__(self, *args: Cmd):
        super().__init__(args)


class Cmd(Node):
    pass
class Print(Cmd):
    def __init__(self, _0: Expr):
        super().__init__((_0,))


class Expr(Node):
    pass
class Lit(Expr):
    def __init__(self, _0: int):
        super().__init__((_0,))
class Add(Expr):
    def __init__(self, *args: Expr):
        super().__init__(args)
class Sub(Expr):
    def __init__(self, _0: Expr, _1: Expr):
        super().__init__((_0, _1))
class Mul(Expr):
    def __init__(self, *args: Expr):
        super().__init__(args)
class Div(Expr):
    def __init__(self, _0: Expr, _1: Expr):
        super().__init__((_0, _1))
class Mod(Expr):
    def __init__(self, _0: Expr, _1: Expr):
        super().__init__((_0, _1))