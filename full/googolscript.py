# Googolscript interpreter
# Version 0.0.0
# Created by Tsskyx

DEBUG = True

import sys
if len(sys.argv) != 2:
    print("Usage: 'python googolscript.py [file].gs'")
    exit(1)
with open("grammar.lark", encoding="utf-8") as file:
    grammar = file.read()
with open(sys.argv[1], encoding="utf-8") as file:
    user_code = file.read()

from lark import Lark
parser = Lark(
    grammar,
    parser = "lalr",
    debug = DEBUG,
    strict = True,
    propagate_positions = True,
    start = "top"
)

from lark.exceptions import UnexpectedInput
try:
    parse_tree = parser.parse(user_code)
except UnexpectedInput as e:
    print(e.get_context(user_code))
    sys.exit(1)

from gs_transformer import transform
parse_tree = transform(parse_tree)