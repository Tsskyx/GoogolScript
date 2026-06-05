type AST = dict[str, dict[str, list[str] | tuple[str, ellipsis]]]


HEADER = \
"""from __future__ import annotations


class Node:
    __match_args__ = ("cons", "args")
    
    def __init__(self, cons: str, args: tuple[object, ...]):
        self.cons = cons
        self.args = args
    
    def __repr__(self):
        return f"{type(self).__name__}.{self.cons}({', '.join(map(repr, self.args))})"


"""

def parse(ast: AST, file: str):
    def parse_method(name: str, args: list[str] | tuple[str, ellipsis]):
        if isinstance(args, tuple):
            return f"""    @classmethod\n    def {name}(cls, *args: {args[0]}):\n        return cls("{name}", args)"""
        elif len(args) == 0:
            return f"""    @classmethod\n    def {name}(cls):\n        return cls("{name}", ())"""
        elif len(args) == 1:
            return f"""    @classmethod\n    def {name}(cls, _0: {args[0]}):\n        return cls("{name}", (_0,))"""
        else:
            params = "".join(f", _{i}: {t}" for i, t in enumerate(args))
            values = f"({", ".join(f'_{i}' for i in range(len(args)))})"
            return f"""    @classmethod\n    def {name}(cls{params}):\n        return cls("{name}", {values})"""

    with open(file, "w") as f:
        f.write(HEADER + "\n\n\n".join(
            f"class {name}(Node):\n" + "\n\n".join(
                parse_method(cons, args) for cons, args in spec.items())
            if len(spec) else "    pass"
            for name, spec in ast.items()) + "\n")
