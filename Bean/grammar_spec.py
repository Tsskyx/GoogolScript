from grammar_gen import AST, parse

prog: AST = {
    "Prog": {"prog": ("Cmd", ...)},
    "Cmd": {"print": ["Expr"]},
    "Expr": {
        "lit": ["int"],
        "add": ("Expr", ...),
        "sub": ["Expr", "Expr"],
        "mul": ("Expr", ...),
        "div": ["Expr", "Expr"],
        "mod": ["Expr", "Expr"],
    }
}

parse(prog, "grammar.py")