import sys
from parser import parse
from evaluator import evaluate

def main():
    match len(sys.argv):
        case 1:
            print("Welcome to the GoogolScript 0.0.2 REPL.")
            print("Commands here will be interpreted the same way as commands from a .gs source file.")
            print("The current exiting keyword is 'EXIT'. For a full grammar specification, see the source code.")
            print("To run code from a .gs source file, you can simply drag-and-drop it onto this script.")
            while evaluate(parse(input("> "))): pass
        case 2:
            with open(sys.argv[1], "r", encoding = "utf-8") as file:
                source = file.read()
            evaluate(parse(source))
        case _: raise Exception("Unexpected number of arguments")

if __name__ == "__main__": main()