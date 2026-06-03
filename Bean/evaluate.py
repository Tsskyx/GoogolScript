from grammar import *
"""
def run_root(root: Root):
    match root:
        case Prog((Cmd(arg), *rest)):
            run_cmd(Cmd(arg))
            x = Prog(tuple(rest))
            run_root(x)
        case _:
            pass
    match root:
        case Prog(args):
            for arg in args:
                match arg:
                    case Cmd():
                        run_cmd(arg)
                    case _:
                        raise TypeError(f"Unknown case: {arg}")
        case _:
            raise TypeError(f"Unknown case: {prog}")

def run_cmd(cmd: Cmd):
    match cmd:
        case Cmd((Expr(args), )):
            print(run_expr(Expr(args)))
        case _:
            raise ValueError(f"Unknown case: {cmd}")

def run_expr(expr: Expr) -> int:
    match expr:
        case Expr("lit", (int(arg),)):
            return arg
        case Expr("add", (Expr(cons, args), *rest)):
            x = run_expr(Expr(cons, args))
            y = run_expr(Expr("add", tuple(rest)))
            return x + y
        case Expr("add", ()):
            return 0
        case Expr("sub", (Expr(cons1, args1), Expr(cons2, args2))):
            x = run_expr(Expr(cons1, args1))
            y = run_expr(Expr(cons2, args2))
            return x - y
        case Expr("mul", (Expr(cons, args), *rest)):
            x = run_expr(Expr(cons, args))
            y = run_expr(Expr("mul", tuple(rest)))
            return x * y
        case Expr("mul", ()):
            return 1
        case Expr("div", (Expr(cons1, args1), Expr(cons2, args2))):
            x = run_expr(Expr(cons1, args1))
            y = run_expr(Expr(cons2, args2))
            return x // y if y != 0 else 0
        case Expr("div", (Expr(cons1, args1), Expr(cons2, args2))):
            x = run_expr(Expr(cons1, args1))
            y = run_expr(Expr(cons2, args2))
            return x % y if y != 0 else 0
        case _:
            raise ValueError(f"Unknown case: {expr}")
"""
prog = \
Prog(
    Print(
        Lit(3),
    ),
    Print(
        Add(
            Lit(5),
            Lit(3),
        ),
    ),
)