from generator import AST, parse

grammar: AST = {
    "Program": {
        "Top": ({"Cmd", "Label"}, ...),
    },
    "Mode": ("IMM", "REG"),
    "Op": ("ADD", "SUB", "MUL", "DIV", "MOD"),
    "Rel": ("EQ", "NE", "LT", "LE", "GT", "GE"),
    "Label": {
        "LABEL": ("str",),
    },
    "Cmd": {
        "MOV": ("Mode", "int", "int"),
        "LOAD": ("int", "int"),
        "STORE": ("int", "int"),
        "OP": ("Op", "Mode", "int", "int", "int"),
        "JMP": ("str",),
        "JIF": ("Rel", "Mode", "int", "int", "str"),
        "READ": ("int",),
        "WRITE": ("int",),
    }
}

parse(grammar, "syntax.py")