from lark import Lark
from lark.exceptions import UnexpectedCharacters, UnexpectedToken, UnexpectedEOF
from transformer import transform
from gs_nodes import GS_Node
from evaluator import evaluate

def main():
    with open("grammar.lark", encoding="utf-8") as file:
        grammar = file.read()
    
    parser = Lark(
        grammar,
        debug = True,
        strict = True,
        propagate_positions = True,
        start = "top"
    )

    print("Welcome to GoogolScript v0.0.1")
    print("For documentation, please refer to the source code.")
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
        except UnexpectedCharacters as e:
            print("Error: unexpected characters\n" + e.get_context(line))
        except UnexpectedToken as e:
            print("Error: unexpected token\n" + e.get_context(line))
        except UnexpectedEOF as e:
            print("Error: unexpected EOF\n" + e.get_context(line))
        except (EOFError, KeyboardInterrupt): # can un-parenthesize in Python 3.14
            break
        except Exception as e:
            print(str(e))

if __name__ == "__main__":
    main()