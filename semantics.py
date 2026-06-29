from syntax import *

mem: dict[int, int] = {}
jmp: dict[int, int] = {}


def R(i: int):
    return 0 if i < 0 else mem.get(i, 0)


def trunc_div(x: int, y: int):
    if y == 0: return 0
    q = abs(x) // abs(y)
    return q if x >= 0 and y >= 0 or x < 0 and y < 0 else -q


def trunc_mod(x: int, y: int):
    if y == 0: return 0
    q = abs(x) % abs(y)
    return q if x >= 0 else -q


def memset(i: int, v: int):
    if i >= 0:
        mem[i] = v


def run(prog: list[Cmd]):
    for i, cmd in enumerate(prog):
        match cmd:
            case LABEL((x,)):
                if x in jmp:
                    raise Exception("Duplicate label")
                jmp[x] = i
            case _:
                pass
    pos: int = 0
    while pos < len(prog):
        match prog[pos]:
            case READ((x,)):
                try:
                    memset(x, int(input()))
                except ValueError:
                    continue
            case WRITE((x,)):
                print(R(x))
            case JMP((i,)):
                pos = jmp.get(i, 0)
            case MOV_C((x, c)):
                memset(x, c)
            case MOV_R((x, y)):
                memset(x, R(y))
            case LOAD((x, y)):
                memset(x, R(R(y)))
            case STORE((x, y)):
                memset(R(x), R(y))
            case ADD_C((x, y, c)):
                memset(x, R(y) + c)
            case ADD_R((x, y, z)):
                memset(x, R(y) + R(z))
            case SUB_C((x, y, c)):
                memset(x, R(y) - c)
            case SUB_R((x, y, z)):
                memset(x, R(y) - R(z))
            case MUL_C((x, y, c)):
                memset(x, R(y) * c)
            case MUL_R((x, y, z)):
                memset(x, R(y) * R(z))
            case DIV_C((x, y, c)):
                memset(x, trunc_div(R(y), c))
            case DIV_R((x, y, z)):
                memset(x, trunc_div(R(y), R(z)))
            case MOD_C((x, y, c)):
                memset(x, trunc_mod(R(y), c))
            case MOD_R((x, y, z)):
                memset(x, trunc_mod(R(y), R(z)))
            case JEQ_C((x, c, i)):
                if R(x) == c:
                    pos = jmp.get(i, 0)
            case JEQ_R((x, y, i)):
                if R(x) == R(y):
                    pos = jmp.get(i, 0)
            case JNE_C((x, c, i)):
                if R(x) != c:
                    pos = jmp.get(i, 0)
            case JNE_R((x, y, i)):
                if R(x) != R(y):
                    pos = jmp.get(i, 0)
            case JLT_C((x, c, i)):
                if R(x) < c:
                    pos = jmp.get(i, 0)
            case JLT_R((x, y, i)):
                if R(x) < R(y):
                    pos = jmp.get(i, 0)
            case JLE_C((x, c, i)):
                if R(x) <= c:
                    pos = jmp.get(i, 0)
            case JLE_R((x, y, i)):
                if R(x) <= R(y):
                    pos = jmp.get(i, 0)
            case JGT_C((x, c, i)):
                if R(x) > c:
                    pos = jmp.get(i, 0)
            case JGT_R((x, y, i)):
                if R(x) > R(y):
                    pos = jmp.get(i, 0)
            case JGE_C((x, c, i)):
                if R(x) >= c:
                    pos = jmp.get(i, 0)
            case JGE_R((x, y, i)):
                if R(x) >= R(y):
                    pos = jmp.get(i, 0)
            case _:
                pass
        pos += 1
