from lark import Transformer
from lark.lexer import Token
from lark.tree import Tree
import gs_implementation as impl
from typing import cast

def get_meta(source):
    meta = source.meta if hasattr(source, "meta") else source
    return meta.line, meta.column, meta.end_line, meta.end_column

class T(Transformer):
    def gs_bool(self, children: list[Token]):
        source = children[0]
        return impl.GS_Bool(source.value, get_meta(source))

    def gs_null(self, children: list[Token]):
        source = children[0]
        return impl.GS_Null(source.value, get_meta(source))

    def gs_string(self, children: list[Tree]):
        source = children[0]
        parts = []
        for child in source.children:
            if isinstance(child, Token):
                if child.type == "str_lit":
                    parts.append(child.value)
                elif child.type == "str_esc":
                    match child.value[1]:
                        case "n": parts.append("\n")
                        case "t": parts.append("\t")
                        case "\"": parts.append("\"")
                        case "{": parts.append("{")
                        case "}": parts.append("}")
                        case "\\": parts.append("\\")
                        case "u": parts.append(chr(int(child.value[2:], 16)))
            elif isinstance(child, Tree):
                if child.data == "str_var":
                    expr = child.children[0]
                    expr_ast = self.transform(expr)
                    parts.append(expr_ast)
        return impl.GS_StringExpr(parts, get_meta(source))
    
    def gs_int(self, children: list[Tree]):
        def d_val(c: str, base):
            if "0" <= c <= "9": return ord(c) - ord("0")
            if "A" <= c <= "Z": return ord(c) - ord("A")
            if "a" <= c <= "z": return ord(c) - ord("a") if base > 36 else ord(c.upper()) - ord("A")
            if c == "$": return 62
            return 63
        
        source: Tree = children[0]
        parts = cast(list[Token], source.children)
        meta = get_meta(source)

        sign_str = parts[0].value
        base_str = parts[1].value
        main_str = parts[2].value
        
        base = int(base_str[:-1]) if bool(base_str) else 10
        if not (2 <= base <= 64): return impl.GS_Error("Invalid syntax", source)

        main = []
        for i, c in enumerate(main_str):
            if c == "'":
                if i == 0 or i == len(main_str)-1 or main_str[i-1] == "'":
                    return impl.GS_Error("Invalid syntax", main_str)
            else:
                d = d_val(c, base)
                if d >= base: return impl.GS_Error("Invalid syntax", main_str)
                main.append(d)
        
        return impl.GS_Int((sign_str, base, main), meta)

def transform(parse_tree): return T().transform(parse_tree)