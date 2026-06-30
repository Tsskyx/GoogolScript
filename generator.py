type FixArgs = tuple[str, ...]
type VarArgs = tuple[set[str], ellipsis]
type Variant = tuple[str, ...]
type Inductive = dict[str, FixArgs | VarArgs]
type AST = dict[str, Inductive | Variant]


HEADER = """from __future__ import annotations
from dataclasses import dataclass


class Node:
    __match_args__ = ()

    def __repr__(self):
        items = (getattr(self, name) for name in type(self).__match_args__)
        return f"{type(self).__name__}({', '.join(map(repr, items))})"


"""

def parse_ind(base: str, name: str, args: FixArgs | VarArgs):
    if len(args) == 2 and isinstance(args[0], set) and args[1] is ...:
        deco = "@dataclass(slots=True, repr=False, init=False)"
        head = f"class {name}({base}):"
        init = f"    def __init__(self, *items: {" | ".join(args[0])}):\n        self.items = items\n"
        iter = f"    def __iter__(self):\n        return iter(self.items)"
        return "\n".join((deco, head, init, iter))
    else:
        deco = "@dataclass(slots=True, repr=False)"
        head = f"class {name}({base}):"
        vars = "\n".join(f"    _{i}: {arg}" for i, arg in enumerate(args)) if args else "    pass"
        return "\n".join((deco, head, vars))

def parse_var(base: str, name: str):
    deco = "@dataclass(slots=True, repr=False)"
    body = f"class {name}({base}):\n    pass"
    return "\n".join((deco, body))

def parse_inductive(name: str, body: Inductive | Variant):
    head = f"class {name}(Node):\n    pass\n\n\n"
    if isinstance(body, dict):
        return head + "\n\n\n".join(parse_ind(name, cons, args) for cons, args in body.items())
    else:
        return head + "\n\n\n".join(parse_var(name, cons) for cons in body)

def parse(grammar: AST, output: str):
    with open(output, "w") as file:
        file.write(HEADER + "\n\n\n".join(parse_inductive(name, body) for name, body in grammar.items()) + "\n")