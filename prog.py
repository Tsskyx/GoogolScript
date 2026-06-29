from syntax import *

# temp variables
TMP_1 = 0
TMP_2 = 1

# input
ROWS = 2
COLS = 3
INDEX = 4

# iteration
X = 5
Y = 6
Z = 7

# array access
M = 8
A = 9
R = 10
L = 11

# computed
TAIL = 12
ROOT = 13

# matrix pointers
ASC = 14 # will point to MEM_START
MAT = 15 # will point to MEM_START + rows * cols (ASC len)

# array alignment constant
MEM_START = MAT + 1

# labels
END_PROG = 0
OUTPUT = 1
SKIP_1 = 2
SKIP_2 = 3
SKIP_3 = 4
SKIP_4 = 5
SKIP_5 = 6
LOOP_1 = 7
END_1 = 8
LOOP_2 = 9
END_2 = 10
LOOP_3 = 11
END_3 = 12
LOOP_4 = 13
END_4 = 14
LOOP_5 = 15
END_5 = 16
LOOP_6 = 17
END_6 = 18
LOOP_7 = 19
END_7 = 20
LOOP_8 = 21
END_8 = 22
LOOP_9 = 23
END_9 = 24
LOOP_10 = 25
END_10 = 26
LOOP_11 = 27
END_11 = 28
LOOP_12 = 29
END_12 = 30

prog: list[Cmd] = [
    READ(ROWS),                 # ROWS := input()
    JLT_C(ROWS, 1, END_PROG),   # if ROWS < 1: goto END_PROG
    READ(COLS),                 # COLS := input()
    JLT_C(COLS, 1, END_PROG),   # if COLS < 1: goto END_PROG
    READ(INDEX),                # INDEX := input()
    JLT_C(INDEX, 0, END_PROG),  # if INDEX < 0: goto END_PROG
    MOV_C(ASC, MEM_START),      # set ASC at MEM_START
    MUL_R(TMP_1, COLS, ROWS),
    ADD_R(MAT, ASC, TMP_1),     # set MAT at MEM_START + COLS * ROWS
    MOV_C(X, 0),
    LABEL(LOOP_1),
    JGE_R(X, TMP_1, END_1),     # for (X := 0; X < COLS * ROWS; X++)
        READ(TMP_2),                # TMP_2 := input()
        JLT_C(TMP_2, 0, END_PROG),  # if TMP_2 < 0: goto END_PROG
        ADD_R(M, MAT, X),
        STORE(M, TMP_2),            # MAT[X] := TMP_2
        ADD_C(X, X, 1),
        JMP(LOOP_1),
    LABEL(END_1),
    SUB_C(TAIL, ROWS, 1),
    LABEL(LOOP_2),
    JLE_C(TAIL, -1, END_2),     # for (TAIL := ROWS - 1; TAIL > -1; TAIL--)
        SUB_C(M, COLS, 1),
        MUL_R(M, M, ROWS),
        ADD_R(M, M, TAIL),
        ADD_R(M, M, MAT),
        LOAD(M, M),                 # M := MAT[COLS - 1, TAIL]
        JGT_C(M, 0, END_2),         # if M > 0: break
        SUB_C(TAIL, TAIL, 1),
        JMP(LOOP_2),
    LABEL(END_2),
    JGT_C(TAIL, -1, SKIP_1),    # if TAIL > -1: goto SKIP_1
    SUB_C(COLS, COLS, 1),       # COLS--
    JMP(OUTPUT),                # goto OUTPUT
    LABEL(SKIP_1),              # SKIP_1
    MOV_C(X, 0),
    LABEL(LOOP_3),
    JGE_R(X, COLS, END_3),      # for (X := 0; X < COLS; X++)
        MOV_C(Y, 0),
        LABEL(LOOP_4),
        JGT_R(Y, TAIL, END_4),      # for (Y := 0; Y <= TAIL; Y++)
            MUL_R(TMP_1, X, ROWS),
            ADD_R(TMP_1, TMP_1, Y),     # TMP_1 := X * ROWS + Y
            ADD_R(M, TMP_1, MAT),
            LOAD(M, M),                 # M := MAT[TMP_1]
            MOV_R(Z, X),                # Z := X
            LABEL(LOOP_5),              # while (true)
                JGT_C(Y, 0, SKIP_2),        # if Y > 0: goto SKIP_2
                SUB_C(Z, Z, 1),             # Z--
                JMP(SKIP_3),                # goto SKIP_3
                LABEL(SKIP_2),              # SKIP_2
                MUL_R(A, Z, ROWS),
                ADD_R(A, A, Y),
                SUB_C(A, A, 1),
                ADD_R(A, A, ASC),
                LOAD(Z, A),                 # Z := ASC[Z, Y - 1]
                LABEL(SKIP_3),              # SKIP_3
                JLE_C(Z, -1, END_5),        # if Z <= -1: break
                MUL_R(R, Z, ROWS),
                ADD_R(R, R, Y),
                ADD_R(R, R, MAT),
                LOAD(R, R),                 # R := MAT[Z, Y]
                JLT_R(R, M, END_5),         # if R < M: break
                JMP(LOOP_5),
            LABEL(END_5),
            ADD_R(A, TMP_1, ASC),
            STORE(A, Z),                # ASC[TMP_1] := Z
            ADD_C(Y, Y, 1),
            JMP(LOOP_4),
        LABEL(END_4),
        ADD_C(X, X, 1),
        JMP(LOOP_3),
    LABEL(END_3),
    SUB_C(A, COLS, 1),
    MUL_R(A, A, ROWS),
    ADD_R(A, A, TAIL),
    ADD_R(A, A, ASC),
    LOAD(ROOT, A),              # ROOT := ASC[COLS - 1, TAIL]
    MOV_C(Y, 0),
    LABEL(LOOP_6),
    JGT_R(Y, TAIL, END_6),      # for (Y := 0; Y <= TAIL; Y++)
        SUB_C(M, COLS, 1),
        MUL_R(M, M, ROWS),
        ADD_R(M, M, Y),
        ADD_R(M, M, MAT),
        LOAD(M, M),                 # M := MAT[COLS - 1, Y]
        MUL_R(TMP_1, ROOT, ROWS),
        ADD_R(TMP_1, TMP_1, Y),     # TMP_1 := ROOT * ROWS + Y
        ADD_R(R, TMP_1, MAT),
        LOAD(R, R),                 # R := MAT[TMP_1]
        ADD_R(A, TMP_1, ASC),
        SUB_R(TMP_2, M, R),
        STORE(A, TMP_2),            # ASC[TMP_1] := M - R
        ADD_C(Y, Y, 1),
        JMP(LOOP_6),
    LABEL(END_6),
    ADD_C(X, ROOT, 1),
    LABEL(LOOP_7),
    JGE_R(X, COLS, END_7),      # for (X := ROOT + 1; X < COLS; X++)
        MOV_C(Y, 0),
        LABEL(LOOP_8),
        JGT_R(Y, TAIL, END_8),      # for (Y := 0; Y <= TAIL; Y++)
            MUL_R(A, X, ROWS),
            ADD_R(A, A, Y),
            ADD_R(A, A, ASC),           # A := &ASC[X, Y]
            LOAD(Z, A),                 # Z := *A
            MOV_C(R, 0),
            JLT_R(Z, ROOT, SKIP_4),     # if Z < ROOT: goto SKIP_4
            MUL_R(R, Z, ROWS),
            ADD_R(R, R, Y),
            ADD_R(R, R, ASC),
            LOAD(R, R),                 # R := ASC[Z, Y]
            LABEL(SKIP_4),              # SKIP_4
            STORE(A, R),                # *A := R
            ADD_C(Y, Y, 1),
            JMP(LOOP_8),
        LABEL(END_8),
        ADD_C(X, X, 1),
        JMP(LOOP_7),
    LABEL(END_7),
    SUB_C(COLS, COLS, 1),       # COLS--
    MOV_R(TMP_1, COLS),         # TMP_1 := COLS
    MOV_C(Z, 1),
    LABEL(LOOP_9),
    JGT_R(Z, INDEX, END_9),     # for (Z := 1; Z <= INDEX; Z++)
        MOV_R(X, ROOT),
        LABEL(LOOP_10),
        JGE_R(X, TMP_1, END_10),    # for (X := ROOT; X < TMP_1; X++)
            MOV_C(Y, 0),
            LABEL(LOOP_11),
            JGE_R(Y, ROWS, END_11),     # for (Y := 0; Y < ROWS; Y++)
                MUL_R(TMP_2, X, ROWS),
                ADD_R(TMP_2, TMP_2, Y),     # TMP_2 := X * ROWS + Y
                ADD_R(M, MAT, TMP_2),
                LOAD(M, M),                 # M := MAT[TMP_2]
                JGE_R(Y, TAIL, SKIP_5),     # if Y >= TAIL: goto SKIP_5
                ADD_R(A, ASC, TMP_2),
                LOAD(A, A),                 # A := ASC[TMP_2]
                MUL_R(A, A, Z),             # A *= Z
                ADD_R(M, M, A),             # M += A
                LABEL(SKIP_5),              # SKIP_5
                MUL_R(L, COLS, ROWS),
                ADD_R(L, L, Y),
                ADD_R(L, L, MAT),
                STORE(L, M),                # MAT[COLS, Y] := M
                ADD_C(Y, Y, 1),
                JMP(LOOP_11),
            LABEL(END_11),
            ADD_C(COLS, COLS, 1),       # COLS++
            ADD_C(X, X, 1),
            JMP(LOOP_10),
        LABEL(END_10),
        ADD_C(Z, Z, 1),
        JMP(LOOP_9),
    LABEL(END_9),
    LABEL(OUTPUT),              # OUTPUT
    MOV_C(X, 0),
    MUL_R(TMP_1, COLS, ROWS),   # TMP_1 := COLS * ROWS
    LABEL(LOOP_12),
    JGE_R(X, TMP_1, END_12),    # for (X := 0; X < TMP_1; X++)
        ADD_R(M, MAT, X),
        LOAD(M, M),                 # M := MAT[X]
        WRITE(M),                   # print(M)
        ADD_C(X, X, 1),
        JMP(LOOP_12),
    LABEL(END_12),
    LABEL(END_PROG),
]

from semantics import run

run(prog)

# [[0,0,0],[1,1,1],[2,0,0],[3,1,0],[1,1,1]]
# [[0,0,0],[1,1,1],[2,0,0],[3,1,0],[1,1,0],[2,2,1],[3,0,0],[4,1,0]]
# [[0,0,0,0],[1,1,1,1],[2,2,2,1],[3,3,2,1],[4,3,2,0],[5,4,3,1],[4,2,2,1],[5,3,2,1]]
# [[0,0,0,0],[1,1,1,1],[2,2,2,1],[3,3,2,1],[4,3,2,0],[5,4,3,1],[4,2,2,1],[5,3,2,0],[6,4,3,1],[7,5,4,1],[8,6,4,1],[9,6,4,0],[10,7,5,1],[9,5,4,1]]