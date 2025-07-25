__all__ = [
    "GS_Top",
    "GS_Node",
    "GS_Null",
    "GS_Bool",
    "GS_Int",
    "GS_String"
]

from abc import ABC as Abstract

class GS_Node(Abstract):
    def __repr__(self) -> str: return str(self)

class GS_Top(GS_Node):
    def __init__(self, child: GS_Node): self.child: GS_Node = child
    def __str__(self) -> str: return str(self.child)

class GS_Null(GS_Node):
    def __init__(self, value: str): self.value: str = value
    def __str__(self) -> str: return self.value

class GS_Bool(GS_Node):
    def __init__(self, value: str): self.value: str = value
    def __str__(self) -> str: return self.value

class GS_Int(GS_Node):
    def __init__(self, value: list[int]): self.value: list[int] = self.encode(value, 10)
    def __str__(self) -> str: return "".join(str(digit) for digit in self.decode(self.value, 10))

    def encode(self, digits: list[int], base: int) -> list[int]:
        def halve(orig: list[int]):
            half = [0] * len(orig)
            r = 0
            for i, d in enumerate(orig):
                half[i], r = divmod(r * base + d, 2)
            return half, r
        temp = []
        while any(digits):
            digits, r = halve(digits)
            temp.append(r)
        while len(temp) and temp[-1] == 0: temp.pop()
        return temp[::-1]

    def decode(self, digits: list[int], base: int) -> list[int]:
        def double(orig: list[int]):
            double = [0] * len(orig)
            c = 0
            for i in reversed(range(len(orig))):
                c, double[i] = divmod(orig[i] * 2 + c, base)
            return [1] + double if c else double
        temp = [0]
        for d in digits:
            temp = double(temp)
            temp[-1] += d
        return temp

class GS_String(GS_Node):
    def __init__(self, value: list[str]): self.value = value
    def __str__(self) -> str: return "".join(self.value)