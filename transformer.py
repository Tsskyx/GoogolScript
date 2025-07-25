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
    
    def int(self, children: list[Token]) -> GS_Int:
        digits = [int(token.value) for token in children]
        return GS_Int(digits)
    
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