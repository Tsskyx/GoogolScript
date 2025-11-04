import sys
from pathlib import Path

def main() -> str:
    args = sys.argv[1:]
    if len(args) == 0:
        return "Error: Missing source-file argument"
    if len(args) > 1:
        return "Error: Too many arguments"
    path = Path(args[0])
    try:
        with open(path, "r", encoding = "utf-8") as file:
            source = file.read()
    except FileNotFoundError:
        return f"Error: file {path} not found"
    except IsADirectoryError:
        return f"Error: {path} is a directory"
    except PermissionError:
        return f"Error: permission to {path} denied"
    except UnicodeError as e:
        return f"Error: {e}"
    except OSError as e:
        return f"Error: {e}"
    
    print(source)

    return ""

if __name__ == "__main__":
    print(main())