r"""
gs_number: num_parts
num_parts:
    /[+-]?/
    /([0-9]+b)?/
    /[0-9'A-Za-z_$]+|INF/
    /(\.[0-9'A-Za-z_$]*)?/
    /(r[0-9'A-Za-z_$]+)?/
    /i?/
"""

"""
def gs_number(self, children: list[Tree]):
    def d_val(c: str, base):
        if "0" <= c <= "9": return ord(c) - ord("0")
        if "A" <= c <= "Z": return ord(c) - ord("A")
        if "a" <= c <= "z": return ord(c) - ord("a") if base > 36 else ord(c.upper()) - ord("A")
        if c == "$": return 62
        return 63
    
    def parse_nums(source):
        res = []
        for i, c in enumerate(source):
            if c == "'":
                if i == 0 or i == len(source)-1 or source[i-1] == "'":
                    return impl.Error("Invalid syntax", source)
            else:
                d = d_val(c, base)
                if d >= base: return impl.Error("Invalid syntax", source)
                res.append(d)
        return res
    
    source: Tree = children[0]
    parts = cast(list[Token], source.children)
    
    sign_part = parts[0].value
    has_sign = bool(sign_part)
    sign = sign_part if has_sign else "+"

    base_part = parts[1].value
    has_base = bool(base_part)
    base = int(base_part[:-1]) if has_base else 10
    if not (2 <= base <= 64): return impl.Error("Invalid syntax", source)

    whole_part = parts[2].value
    is_inf = whole_part == "INF"
    if is_inf and has_base: return impl.Error("Invalid syntax", source)
    whole = [] if is_inf else parse_nums(whole_part)

    frac_part, rep_part = parts[3].value, parts[4].value
    has_frac, has_rep = bool(frac_part), bool(rep_part)
    if is_inf and (has_frac or has_rep): return impl.Error("Invalid syntax", source)
    if frac_part == "." and not has_rep: return impl.Error("Invalid syntax", source)
    if not has_frac and has_rep: return impl.Error("Invalid syntax", source)
    frac = parse_nums(frac_part[1:])
    rep = parse_nums(rep_part[1:])
    
    im_part = parts[5].value 
    is_im = bool(im_part)
    if is_inf and is_im: return impl.Error("Invalid syntax", source)
    
    parts = (sign, base, is_inf, whole, frac, rep, is_im)
    return impl.Number(parts, source)
"""

"""
class Number:
    def __init__(self, parts, source):
        self.meta = extract_meta(source)
        self.sign, base, self.is_inf, whole, frac, rep, self.is_im = parts
        whole, frac, rep = Number.normalize(whole, frac, rep, base)
        self.whole, self.frac, self.rep = Number.to_binary(whole, frac, rep, base)
    
    @staticmethod
    def to_binary(whole: list, frac: list, rep: list, base):
        def whole_to_binary(whole: list, base):
            def whole_halve(whole: list, base):
                temp = []
                c, r = divmod(whole[0], 2)
                if c: temp.append(c)
                for d in whole[1:]:
                    c, r = divmod(base * r + d, 2)
                    temp.append(c)
                return temp, r
            temp = []
            while whole != [0]:
                whole, r = whole_halve(whole, base)
                temp.append(r)
            return temp[::-1] if temp else [0]
        def frac_to_binary(frac: list, rep: list, base):
            def frac_double(frac: list, rep: list, base):
                temp = []
                r = 0
                last = rep[0] if rep else 0
                for d in frac + rep + [last]:
                    c, r = divmod(r * base + d * 2, base)
                    temp.append(c)
                return temp[0], temp[1:len(frac)+1], temp[len(frac)+1:]
            temp = []
            seen = dict()
            while (state := (tuple(frac), tuple(rep))) not in seen:
                seen[state] = len(temp)
                carry, frac, rep = frac_double(frac, rep, base)
                temp.append(carry)
            return temp[:seen[state]], temp[seen[state]:]
        whole = whole_to_binary(whole, base)
        frac, rep = frac_to_binary(frac, rep, base)
        return Number.normalize(whole, frac, rep, base)
    
    @staticmethod
    def from_binary(whole: list, frac: list, rep: list, base):
        def whole_from_binary(whole: list, base):
            def whole_double(whole: list, base):
                temp = []
                c = 0
                for d in reversed(whole):
                    c, r = divmod(d * 2 + c, base)
                    temp.append(r)
                if c: temp.append(c)
                return temp[::-1]
            temp = [0]
            for d in whole:
                temp = whole_double(temp, base)
                temp[-1] += d
            return temp
        def frac_from_binary(frac: list, rep: list, base):
            def frac_mult(frac: list, rep: list, n):
                def to_bin(d):
                    temp = []
                    while d:
                        d, r = divmod(d, 2)
                        temp.append(r)
                    return temp[::-1]
                def add_at(A: list, B: list, n):
                    for i in range(len(B)):
                        if 0 <= n-i < len(A): A[n-i] += B[-1-i]
                N = to_bin(n)
                temp = [0] * (len(N) + len(frac) + len(rep))
                for i in range(len(frac) + len(rep) + (len(N)-1) * bool(len(rep))):
                    d = frac[i] if i < len(frac) else rep[(i-len(frac)) % len(rep)]
                    if d: add_at(temp, N, len(N)+i)
                while any(d > 1 for d in temp):
                    D = len(to_bin(max(temp)))
                    new = [0] * len(temp)
                    for i in range(len(temp) + D - 1):
                        d = temp[i] if i < len(temp) else temp[-len(rep) + (i-len(temp)) % len(rep)]
                        add_at(new, to_bin(d), i)
                    temp = new
                return temp[:len(N)], temp[len(N):len(N)+len(frac)], temp[len(N)+len(frac):]
            def to_dec(bin: list):
                dec = 0
                for d in bin: dec = dec * 2 + d
                return dec
            temp = []
            seen = dict()
            while (state := (tuple(frac), tuple(rep))) not in seen:
                seen[state] = len(temp)
                whole, frac, rep = frac_mult(frac, rep, base)
                temp.append(to_dec(whole))
            return temp[:seen[state]], temp[seen[state]:]
        whole = whole_from_binary(whole, base)
        frac, rep = frac_from_binary(frac, rep, base)
        return Number.normalize(whole, frac, rep, base)
    
    @staticmethod
    def normalize(whole: list, frac: list, rep: list, base):
        def whole_add(A: list, B: list, base):
            result = []
            carry = 0
            i, j = len(A) - 1, len(B) - 1
            while i >= 0 or j >= 0 or carry:
                a = A[i] if i >= 0 else 0
                b = B[j] if j >= 0 else 0
                carry, r = divmod(a + b + carry, base)
                result.append(r)
                i -= 1
                j -= 1
            return result[::-1]
        while len(whole) > 1 and whole[0] == 0: whole.pop(0)
        while frac and rep and frac[-1] == rep[-1]:
            rep = [frac.pop()] + rep[:-1]
        for size in range(1, len(rep) + 1):
            chunk = rep[:size]
            if chunk * (len(rep) // size) == rep:
                rep = chunk
                break
        if rep == [base-1]:
            rep = []
            if frac:
                frac[-1] += 1
            else:
                whole = whole_add(whole, [1], base)
        if rep:
            if rep == [0]: rep = []
        else:
            while len(frac) and frac[-1] == 0: frac.pop()
        return whole, frac, rep

    def repr(self, base):
        def d_char(i):
            if i < 10: return chr(ord("0") + i)
            if i < 36: return chr(ord("A") + i - 10)
            if i < 62: return chr(ord("a") + i - 36)
            if i == 63: return "$"
            return "_"
        if self.is_inf: return self.sign + "INF"
        if base <= 64:
            def arr_to_str(arr): return "".join(d_char(i) for i in arr)
            whole, frac, rep = Number.from_binary(self.whole, self.frac, self.rep, base)
            base_repr = "" if base == 10 else f"{base}b"
            whole = arr_to_str(whole)
            frac = "." + arr_to_str(frac) if frac else ""
            rep = ("r" if frac else ".r") + arr_to_str(rep) if rep else ""
            i = "i" if self.is_im else ""
            return self.sign + base_repr + whole + frac + rep + i
        else:
            return str({
                "sign": self.sign,
                "base": base,
                "whole": self.whole,
                "frac": self.frac,
                "rep": self.rep,
                "co": "im" if self.is_im else "re"
            })
"""