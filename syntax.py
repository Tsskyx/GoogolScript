from __future__ import annotations


class Node:
    __match_args__ = ("args",)

    def __init__(self, *args: int):
        self.args = args

    def __len__(self):
        return len(self.args)

    def __getitem__(self, key: int):
        return self.args[key]

    def __repr__(self):
        return f"{type(self).__name__}({', '.join(map(repr, self.args))})"


class Cmd(Node):
    pass


class READ(Cmd):
    def __init__(self, _0: int):
        super().__init__(_0)


class WRITE(Cmd):
    def __init__(self, _0: int):
        super().__init__(_0)


class LABEL(Cmd):
    def __init__(self, _0: int):
        super().__init__(_0)


class JMP(Cmd):
    def __init__(self, _0: int):
        super().__init__(_0)


class MOV_C(Cmd):
    def __init__(self, _0: int, _1: int):
        super().__init__(_0, _1)


class MOV_R(Cmd):
    def __init__(self, _0: int, _1: int):
        super().__init__(_0, _1)


class LOAD(Cmd):
    def __init__(self, _0: int, _1: int):
        super().__init__(_0, _1)


class STORE(Cmd):
    def __init__(self, _0: int, _1: int):
        super().__init__(_0, _1)


class ADD_C(Cmd):
    def __init__(self, _0: int, _1: int, _2: int):
        super().__init__(_0, _1, _2)


class ADD_R(Cmd):
    def __init__(self, _0: int, _1: int, _2: int):
        super().__init__(_0, _1, _2)


class SUB_C(Cmd):
    def __init__(self, _0: int, _1: int, _2: int):
        super().__init__(_0, _1, _2)


class SUB_R(Cmd):
    def __init__(self, _0: int, _1: int, _2: int):
        super().__init__(_0, _1, _2)


class MUL_C(Cmd):
    def __init__(self, _0: int, _1: int, _2: int):
        super().__init__(_0, _1, _2)


class MUL_R(Cmd):
    def __init__(self, _0: int, _1: int, _2: int):
        super().__init__(_0, _1, _2)


class DIV_C(Cmd):
    def __init__(self, _0: int, _1: int, _2: int):
        super().__init__(_0, _1, _2)


class DIV_R(Cmd):
    def __init__(self, _0: int, _1: int, _2: int):
        super().__init__(_0, _1, _2)


class MOD_C(Cmd):
    def __init__(self, _0: int, _1: int, _2: int):
        super().__init__(_0, _1, _2)


class MOD_R(Cmd):
    def __init__(self, _0: int, _1: int, _2: int):
        super().__init__(_0, _1, _2)


class JEQ_C(Cmd):
    def __init__(self, _0: int, _1: int, _2: int):
        super().__init__(_0, _1, _2)


class JEQ_R(Cmd):
    def __init__(self, _0: int, _1: int, _2: int):
        super().__init__(_0, _1, _2)


class JNE_C(Cmd):
    def __init__(self, _0: int, _1: int, _2: int):
        super().__init__(_0, _1, _2)


class JNE_R(Cmd):
    def __init__(self, _0: int, _1: int, _2: int):
        super().__init__(_0, _1, _2)


class JLT_C(Cmd):
    def __init__(self, _0: int, _1: int, _2: int):
        super().__init__(_0, _1, _2)


class JLT_R(Cmd):
    def __init__(self, _0: int, _1: int, _2: int):
        super().__init__(_0, _1, _2)


class JLE_C(Cmd):
    def __init__(self, _0: int, _1: int, _2: int):
        super().__init__(_0, _1, _2)


class JLE_R(Cmd):
    def __init__(self, _0: int, _1: int, _2: int):
        super().__init__(_0, _1, _2)


class JGT_C(Cmd):
    def __init__(self, _0: int, _1: int, _2: int):
        super().__init__(_0, _1, _2)


class JGT_R(Cmd):
    def __init__(self, _0: int, _1: int, _2: int):
        super().__init__(_0, _1, _2)


class JGE_C(Cmd):
    def __init__(self, _0: int, _1: int, _2: int):
        super().__init__(_0, _1, _2)


class JGE_R(Cmd):
    def __init__(self, _0: int, _1: int, _2: int):
        super().__init__(_0, _1, _2)
