from syntax import *

mem: dict[int, int] = {}
jmp: dict[str, int] = {}

def R(i: int):
    return 0 if i < 0 else mem.get(i, 0)

def memset(i: int, v: int):
    if i >= 0:
        mem[i] = v

def trunc_div(x: int, y: int):
    if y == 0: return 0
    q = abs(x) // abs(y)
    return q if x >= 0 and y >= 0 or x < 0 and y < 0 else -q

def trunc_mod(x: int, y: int):
    if y == 0: return 0
    q = abs(x) % abs(y)
    return q if x >= 0 else -q

def decode(mode: Mode, val: int):
    match mode:
        case IMM(): return val
        case REG(): return R(val)
        case _: raise Exception("Invalid Term")

def run(prog: Top):
    cmds: list[Cmd] = []
    for item in prog:
        match item:
            case Cmd():
                cmds.append(item)
            case LABEL(label):
                if label in jmp:
                    raise Exception("Duplicate label")
                jmp[label] = len(cmds)
            case _:
                raise Exception("Invalid term")
    pos: int = 0
    while pos < len(cmds):
        match cmds[pos]:
            case MOV(mode, dst, src):
                memset(dst, decode(mode, src))
            case LOAD(dst, src):
                memset(dst, R(R(src)))
            case STORE(dst, src):
                memset(R(dst), R(src))
            case OP(op, mode, dst, x, y):
                val = decode(mode, y)
                match op:
                    case ADD(): memset(dst, R(x) + val)
                    case SUB(): memset(dst, R(x) - val)
                    case MUL(): memset(dst, R(x) * val)
                    case DIV(): memset(dst, trunc_div(R(x), val))
                    case MOD(): memset(dst, trunc_mod(R(x), val))
                    case _: raise Exception("Invalid Term")
            case JMP(label):
                pos = jmp[label]; continue
            case JIF(rel, mode, x, y, label):
                val = decode(mode, y)
                match rel:
                    case EQ(): pos = jmp[label] - 1 if R(x) == val else pos
                    case NE(): pos = jmp[label] - 1 if R(x) != val else pos
                    case LT(): pos = jmp[label] - 1 if R(x) < val else pos
                    case LE(): pos = jmp[label] - 1 if R(x) <= val else pos
                    case GT(): pos = jmp[label] - 1 if R(x) > val else pos
                    case GE(): pos = jmp[label] - 1 if R(x) >= val else pos
                    case _: raise Exception("Invalid Term")
            case READ(int(dst)):
                try: memset(dst, int(input()))
                except ValueError: continue
            case WRITE(int(dst)):
                print(R(dst))
            case _:
                raise Exception("Invalid term")
        pos += 1