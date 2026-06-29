from grammar import grammar

HEADER = \
"""from __future__ import annotations


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


"""

def parse_cons(name: str, cons: str, argc: int):
    decl = f"class {cons}({name}):\n"
    decl_args = "".join(f", _{i}: int" for i in range(argc))
    call_args = ", ".join(f"_{i}" for i in range(argc))
    init = f"    def __init__(self{decl_args}):\n"
    call = f"        super().__init__({call_args})\n"
    return decl + init + call

def parse_type(name: str, body: dict[str, int]):
    base = f"class {name}(Node):\n    pass\n\n\n"
    return base + "\n\n".join(parse_cons(name, cons, argc) for cons, argc in body.items())

with open("syntax.py", "w") as dst:
    dst.write(HEADER + "\n\n\n".join(parse_type(name, body) for name, body in grammar.items()))