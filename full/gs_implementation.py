class GS_Error:
    def __init__(self, value, meta):
        self.row, self.col, self.rowend, self.colend = meta
        self.value = value

class GS_Bool:
    def __init__(self, value, meta):
        self.row, self.col, self.rowend, self.colend = meta
        self.value = value

class GS_Null:
    def __init__(self, value, meta):
        self.row, self.col, self.rowend, self.colend = meta
        self.value = value

class GS_Int:
    def __init__(self, parts, meta):
        self.row, self.col, self.rowend, self.colend = meta
        sign, base, digits = parts
        self.digits = self.to_binary(digits, base)
        self.is_neg = sign == "-" and self.digits
    
    def to_binary(self, digits: list[int], base: int) -> list[int]:
        def halve(orig: list[int]):
            half = [0] * len(orig)
            r = 0
            for i, d in enumerate(orig):
                half[i], r = divmod(r * base + d, 2)
            return half, r
        temp = []
        while digits != [0]:
            digits, r = halve(digits)
            temp.append(r)
        while len(temp) and temp[-1] == 0: temp.pop()
        return temp[::-1]
    
    def from_binary(self, digits: list[int], base: int) -> list[int]:
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

    def repr(self, base: int):
        def d_char(i):
            if i < 10: return chr(ord("0") + i)
            if i < 36: return chr(ord("A") + i - 10)
            if i < 62: return chr(ord("a") + i - 36)
            if i == 63: return "$"
            if i == 64: return "_"
            return str(i)
        sign_str = "-" if self.is_neg else ""
        base_str = "" if base == 10 else f"{base}b"
        int_str = [d_char(i) for i in self.from_binary(self.digits, base)]
        int_str = "".join(int_str) if base <= 64 else "(" + ".".join(int_str) + ")"
        return sign_str + base_str + int_str

class GS_StringExpr:
    def __init__(self, parts, meta):
        self.parts = parts
        self.row, self.col, self.rowend, self.colend = meta