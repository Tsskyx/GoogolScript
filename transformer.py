from lark import Transformer
from lark.tree import Tree
from lark.lexer import Token
from gs_nodes import *

class GS_Transformer(Transformer):
    def top(self, children: list[GS_Node]) -> GS_Top:
        return GS_Top(children[0])

    def null(self, children: list[Token]) -> GS_Null:
        return GS_Null(children[0].value)
    
    def bool(self, children: list[Token]) -> GS_Bool:
        return GS_Bool(children[0].value)

    def b_int(self, children: list[Token]) -> GS_Int:
        sign, base, main = "+", "10", ""
        for token in children:
            value: str = token.value
            match token.type:
                case "SIGN": sign = value
                case "BASE": base = value
                case "INT10": main = value
                case "INT64": main = value
        return GS_Int(sign, base, main)
    
    def string(self, children: list[Token]) -> GS_String:
        chars: list[str] = []
        for token in children:
            match token.type:
                case "STD_CHAR": chars.append(token.value)
                case "HEX_CODE": chars.append(chr(int(token.value, 16)))
                case "ESC_CHAR":
                    match token.value:
                        case "n": chars.append("\n")
                        case "t": chars.append("\t")
                        case "\"": chars.append("\"")
                        case "\\": chars.append("\\")
        return GS_String(chars)

def transform(parse_tree: Tree) -> GS_Node:
    return GS_Transformer().transform(parse_tree)