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

# find a way to handle errors properly
# like a GS_Node dispatch method before actually initializing the final node object
class GS_Int(GS_Node):
    def __init__(self, sign_str: str, base_str: str, main_str: str):
        def get_digit(c: str, base: int) -> int:
            if "0" <= c <= "9": return ord(c) - ord("0")
            if "A" <= c <= "Z": return ord(c) - ord("A")
            if "a" <= c <= "z": return ord(c) - ord("a") if base > 36 else ord(c.upper()) - ord("A")
            if c == "$": return 62
            if c == "_": return 63
            raise SyntaxError("Syntax error: The grammar was correct, but this GS code is invalid!")
        base = int(base_str) if base_str else 10
        if not 2 <= base <= 64:
            raise SyntaxError("Syntax error: The grammar was correct, but this GS code is invalid!")
        value = []
        for c in main_str:
            if c == "'": continue
            d = get_digit(c, base)
            if d >= base:
                raise SyntaxError("Syntax error: The grammar was correct, but this GS code is invalid!")
            value.append(d)
        self.value = self.encode(value, base)
        self.neg = sign_str == "-" and self.value != []

    def __str__(self) -> str: return ("-" if self.neg else "") + "".join(str(digit) for digit in self.decode(self.value))

    def encode(self, digits: list[int], base: int = 10) -> list[int]:
        def halve(orig: list[int]):
            half = [0] * len(orig)
            r = 0
            for i, d in enumerate(orig):
                half[i], r = divmod(r * base + d, 2)
            return half, r
        for i in range(len(digits)):
            if digits[i]:
                digits = digits[i:]
                break
        else:
            digits = []
        temp = []
        while digits:
            digits, r = halve(digits)
            temp.append(r)
            if not digits[0]: digits.pop(0)
        return temp[::-1]

    def decode(self, digits: list[int], base: int = 10) -> list[int]:
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