from syntax import *
from semantics import run

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

program = Top(
    READ(ROWS),                                       # ROWS := input()
    JIF(LT(), IMM(), ROWS, 1, "END_PROG"),            # if ROWS < 1: goto END_PROG
    READ(COLS),                                       # COLS := input()
    JIF(LT(), IMM(), COLS, 1, "END_PROG"),            # if COLS < 1: goto END_PROG
    READ(INDEX),                                      # INDEX := input()
    JIF(LT(), IMM(), INDEX, 0, "END_PROG"),           # if INDEX < 0: goto END_PROG
    MOV(IMM(), ASC, MEM_START),                       # &ASC := MEM_START
    OP(MUL(), REG(), TMP_1, COLS, ROWS),              # 
    OP(ADD(), REG(), MAT, ASC, TMP_1),                # &MAT := MEM_START + COLS * ROWS
    MOV(IMM(), X, 0),                                 # 
    LABEL("LOOP_1"),                                  # 
    JIF(GE(), REG(), X, TMP_1, "END_1"),              # for (X := 0; X < COLS * ROWS; X++):
        READ(TMP_2),                                  #     TMP_2 := input()
        JIF(LT(), IMM(), TMP_2, 0, "END_PROG"),       #     if TMP_2 < 0: goto END_PROG
        OP(ADD(), REG(), M, MAT, X),                  #     
        STORE(M, TMP_2),                              #     MAT[X] := TMP_2
        OP(ADD(), IMM(), X, X, 1),                    #     
        JMP("LOOP_1"),                                #     
    LABEL("END_1"),                                   # end
    OP(SUB(), IMM(), TAIL, ROWS, 1),                  # 
    LABEL("LOOP_2"),                                  # 
    JIF(LT(), IMM(), TAIL, 0, "END_2"),               # for (TAIL := ROWS - 1; TAIL >= 0; TAIL--):
        OP(SUB(), IMM(), M, COLS, 1),                 #     
        OP(MUL(), REG(), M, M, ROWS),                 #     
        OP(ADD(), REG(), M, M, TAIL),                 #     
        OP(ADD(), REG(), M, M, MAT),                  #     
        LOAD(M, M),                                   #     M := MAT[COLS - 1, TAIL]
        JIF(GT(), IMM(), M, 0, "END_2"),              #     if M > 0: break
        OP(SUB(), IMM(), TAIL, TAIL, 1),              #     
        JMP("LOOP_2"),                                #     
    LABEL("END_2"),                                   # end
    JIF(GE(), IMM(), TAIL, 0, "SKIP_1"),              # if TAIL < 0:
        OP(SUB(), IMM(), COLS, COLS, 1),              #     COLS--
        JMP("OUTPUT"),                                #     goto OUTPUT
    LABEL("SKIP_1"),                                  # end
    MOV(IMM(), X, 0),                                 # 
    LABEL("LOOP_3"),                                  # 
    JIF(GE(), REG(), X, COLS, "END_3"),               # for (X := 0; X < COLS; X++):
        MOV(IMM(), Y, 0),                             #     
        LABEL("LOOP_4"),                              #     
        JIF(GT(), REG(), Y, TAIL, "END_4"),           #     for (Y := 0; Y <= TAIL; Y++):
            OP(MUL(), REG(), TMP_1, X, ROWS),         #         
            OP(ADD(), REG(), TMP_1, TMP_1, Y),        #         TMP_1 := X * ROWS + Y
            OP(ADD(), REG(), M, TMP_1, MAT),          #         
            LOAD(M, M),                               #         M := MAT[TMP_1]
            MOV(REG(), Z, X),                         #         Z := X
            LABEL("LOOP_5"),                          #         while (true):
                JIF(NE(), IMM(), Y, 0, "SKIP_2"),     #             if Y == 0:
                    OP(SUB(), IMM(), Z, Z, 1),        #                 Z--
                    JMP("SKIP_3"),                    #                 
                LABEL("SKIP_2"),                      #                 
                    OP(MUL(), REG(), A, Z, ROWS),     #             else:
                    OP(ADD(), REG(), A, A, Y),        #                 
                    OP(SUB(), IMM(), A, A, 1),        #                 
                    OP(ADD(), REG(), A, A, ASC),      #                 
                    LOAD(Z, A),                       #                 Z := ASC[Z, Y - 1]
                LABEL("SKIP_3"),                      #             end
                JIF(LE(), IMM(), Z, -1, "END_5"),     #             if Z <= -1: break
                OP(MUL(), REG(), R, Z, ROWS),         #             
                OP(ADD(), REG(), R, R, Y),            #             
                OP(ADD(), REG(), R, R, MAT),          #             
                LOAD(R, R),                           #             
                JIF(LT(), REG(), R, M, "END_5"),      #             if MAT[Z, Y] < M: break
                JMP("LOOP_5"),                        #             
            LABEL("END_5"),                           #         end
            OP(ADD(), REG(), A, TMP_1, ASC),          #         
            STORE(A, Z),                              #         ASC[TMP_1] := Z
            OP(ADD(), IMM(), Y, Y, 1),                #         
            JMP("LOOP_4"),                            #         
        LABEL("END_4"),                               #     end
        OP(ADD(), IMM(), X, X, 1),                    #     
        JMP("LOOP_3"),                                #     
    LABEL("END_3"),                                   # end
    OP(SUB(), IMM(), A, COLS, 1),                     # 
    OP(MUL(), REG(), A, A, ROWS),                     # 
    OP(ADD(), REG(), A, A, TAIL),                     # 
    OP(ADD(), REG(), A, A, ASC),                      # 
    LOAD(ROOT, A),                                    # ROOT := ASC[COLS - 1, TAIL]
    MOV(IMM(), Y, 0),                                 # 
    LABEL("LOOP_6"),                                  # 
    JIF(GT(), REG(), Y, TAIL, "END_6"),               # for (Y := 0; Y <= TAIL; Y++):
        OP(SUB(), IMM(), M, COLS, 1),                 #     
        OP(MUL(), REG(), M, M, ROWS),                 #     
        OP(ADD(), REG(), M, M, Y),                    #     
        OP(ADD(), REG(), M, M, MAT),                  #     
        LOAD(M, M),                                   #     M := MAT[COLS - 1, Y]
        OP(MUL(), REG(), TMP_1, ROOT, ROWS),          #     
        OP(ADD(), REG(), TMP_1, TMP_1, Y),            #     TMP_1 := ROOT * ROWS + Y
        OP(ADD(), REG(), R, TMP_1, MAT),              #     
        LOAD(R, R),                                   #     R := MAT[TMP_1]
        OP(ADD(), REG(), A, TMP_1, ASC),              #     
        OP(SUB(), REG(), TMP_2, M, R),                #     
        STORE(A, TMP_2),                              #     ASC[TMP_1] := M - R
        OP(ADD(), IMM(), Y, Y, 1),                    #     
        JMP("LOOP_6"),                                #     
    LABEL("END_6"),                                   # end
    OP(ADD(), IMM(), X, ROOT, 1),                     # 
    LABEL("LOOP_7"),                                  # 
    JIF(GE(), REG(), X, COLS, "END_7"),               # for (X := ROOT + 1; X < COLS; X++):
        MOV(IMM(), Y, 0),                             #     
        LABEL("LOOP_8"),                              #     
        JIF(GT(), REG(), Y, TAIL, "END_8"),           #     for (Y := 0; Y <= TAIL; Y++):
            OP(MUL(), REG(), A, X, ROWS),             #         
            OP(ADD(), REG(), A, A, Y),                #         
            OP(ADD(), REG(), A, A, ASC),              #         A := &ASC[X, Y]
            LOAD(Z, A),                               #         Z := *A
            MOV(IMM(), R, 0),                         #         R := 0
            JIF(LT(), REG(), Z, ROOT, "SKIP_4"),      #         if Z >= ROOT:
                OP(MUL(), REG(), R, Z, ROWS),         #             
                OP(ADD(), REG(), R, R, Y),            #             
                OP(ADD(), REG(), R, R, ASC),          #             
                LOAD(R, R),                           #             R := ASC[Z, Y]
            LABEL("SKIP_4"),                          #         end
            STORE(A, R),                              #         *A := R
            OP(ADD(), IMM(), Y, Y, 1),                #         
            JMP("LOOP_8"),                            #         
        LABEL("END_8"),                               #     end
        OP(ADD(), IMM(), X, X, 1),                    #     
        JMP("LOOP_7"),                                #     
    LABEL("END_7"),                                   # end
    OP(SUB(), IMM(), COLS, COLS, 1),                  # COLS--
    MOV(REG(), TMP_1, COLS),                          # TMP_1 := COLS
    MOV(IMM(), Z, 1),                                 # 
    LABEL("LOOP_9"),                                  # 
    JIF(GT(), REG(), Z, INDEX, "END_9"),              # for (Z := 1; Z <= INDEX; Z++):
        MOV(REG(), X, ROOT),                          #     
        LABEL("LOOP_10"),                             #     
        JIF(GE(), REG(), X, TMP_1, "END_10"),         #     for (X := ROOT; X < TMP_1; X++):
            MOV(IMM(), Y, 0),                         #         
            LABEL("LOOP_11"),                         #         
            JIF(GE(), REG(), Y, ROWS, "END_11"),      #         for (Y := 0; Y < ROWS; Y++):
                OP(MUL(), REG(), TMP_2, X, ROWS),     #             
                OP(ADD(), REG(), TMP_2, TMP_2, Y),    #             TMP_2 := X * ROWS + Y
                OP(ADD(), REG(), M, MAT, TMP_2),      #             
                LOAD(M, M),                           #             M := MAT[TMP_2]
                JIF(GE(), REG(), Y, TAIL, "SKIP_5"),  #             if Y < TAIL:
                    OP(ADD(), REG(), A, ASC, TMP_2),  #                 
                    LOAD(A, A),                       #                 A := ASC[TMP_2]
                    OP(MUL(), REG(), A, A, Z),        #                 A *= Z
                    OP(ADD(), REG(), M, M, A),        #                 M += A
                LABEL("SKIP_5"),                      #             end
                OP(MUL(), REG(), L, COLS, ROWS),      #             
                OP(ADD(), REG(), L, L, Y),            #             
                OP(ADD(), REG(), L, L, MAT),          #             
                STORE(L, M),                          #             MAT[COLS, Y] := M
                OP(ADD(), IMM(), Y, Y, 1),            #             
                JMP("LOOP_11"),                       #             
            LABEL("END_11"),                          #         end
            OP(ADD(), IMM(), COLS, COLS, 1),          #         COLS++
            OP(ADD(), IMM(), X, X, 1),                #         
            JMP("LOOP_10"),                           #         
        LABEL("END_10"),                              #     end
        OP(ADD(), IMM(), Z, Z, 1),                    #     
        JMP("LOOP_9"),                                #     
    LABEL("END_9"),                                   # end
    LABEL("OUTPUT"),                                  # OUTPUT:
    MOV(IMM(), X, 0),                                 # 
    OP(MUL(), REG(), TMP_1, COLS, ROWS),              # 
    LABEL("LOOP_12"),                                 # 
    JIF(GE(), REG(), X, TMP_1, "END_12"),             # for (X := 0; X < COLS * ROWS; X++):
        OP(ADD(), REG(), M, MAT, X),                  #     
        LOAD(M, M),                                   #     M := MAT[X]
        WRITE(M),                                     #     print(M)
        OP(ADD(), IMM(), X, X, 1),                    #     
        JMP("LOOP_12"),                               #     
    LABEL("END_12"),                                  # end
    LABEL("END_PROG"),                                # END_PROG:
)

run(program)