from lark import Lark
from lark.exceptions import UnexpectedInput
from transformer import transform
from gs_nodes import GS_Node
from evaluator import evaluate

def main():
    with open("grammar.lark", encoding="utf-8") as file:
        grammar = file.read()
    
    parser = Lark(
        grammar,
        parser = "lalr",
        debug = True,
        strict = True,
        propagate_positions = True,
        start = "top"
    )

    print("Welcome to GoogolScript v0.0.0")
    print("For documentation, please refer to the grammar file.")
    print("Type 'exit' or 'quit' to leave.")
    print("Made by Tsskyx")

    while True:
        line = input("> ").strip()
        if not line: continue
        if line.lower() in {"exit", "quit"}: break
        try:
            parse_tree = parser.parse(line)
            gs_tree = transform(parse_tree)
            result: GS_Node = evaluate(gs_tree)
            print(str(result))
        except UnexpectedInput as e:
            print(e.get_context(line))
        except (EOFError, KeyboardInterrupt): # can un-parenthesize in Python 3.14
            break
        except Exception as e:
            print(str(e))

if __name__ == "__main__":
    main()