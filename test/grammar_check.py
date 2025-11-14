"""
from grammar import grammar
from parser import table as parse_table

def main() -> int:
    table = parse_table(grammar)
    for key, val in table.items():
        if len(val) > 1:
            print("Collision detected:")
            for prod in val:
                print(f"NT, T: {key}, production: {prod}")
    return 0

if __name__ == "__main__":
    main()
"""