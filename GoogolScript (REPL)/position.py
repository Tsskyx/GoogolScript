from lark.tree import Tree
from lark.tree import Meta
from lark.lexer import Token
from dataclasses import dataclass

@dataclass
class Position: row: int; col: int; row_end: int; col_end: int

def get_position(node: Token | Tree | Meta) -> Position:
    match node:
        case Meta(): return Position(node.line, node.column, node.end_line, node.end_column)
        case Tree(): return Position(node.meta.line, node.meta.column, node.meta.end_line, node.meta.end_column)
        case Token():
            if node.line is not None and node.column is not None and node.end_line is not None and node.end_column is not None:
                return Position(node.line, node.column, node.end_line, node.end_column)
    raise TypeError