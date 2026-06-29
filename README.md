# Bean

Bean is a high-level programming language designed primarily with aesthetics in mind, and based on languages such as Python, JavaScript and OCaml.

The name is a reference to Lean, a particularly elegant proof assistant, and to Mr. Bean, whose comedy transcends language.

## 0.0.0

This is an implementation of a very basic random access machine

Memory (denoted as 'R' below) is stored as a `dict[int, int]` - a map from addresses to values

A jump table is implemented as a `dict[int, int]` - a map from labels to code positions

A program in this version is a simple list of instructions

Available instructions (30):

```
- READ(x): read a value from user input and store it in R[x]
- WRITE(x): write from R[x] to output
- LABEL(x): define a label with a name x (which is an int)
- JMP(x): instead of jumping to the next instruction after this one, jump to the one with label x instead
- MOV_C(x, c): store c in R[x]
- MOV_R(x, y): store R[y] in R[x]
- LOAD(x, y): store the value R[R[y]] in R[x]
- STORE(x, y): store the value R[y] in R[R[x]]
- ADD_C(x, y, c): store [y] +  c  in [x]
- ADD_R(x, y, z): store [y] + [z] in [x]
- SUB_C(x, y, c): store [y] -  c  in [x]
- SUB_R(x, y, z): store [y] - [z] in [x]
- MUL_C(x, y, c): store [y] *  c  in [x]
- MUL_R(x, y, z): store [y] * [z] in [x]
- DIV_C(x, y, c): store [y] /  c  in [x] (rounded towards 0, equals 0 if  c  = 0)
- DIV_R(x, y, z): store [y] / [z] in [x] (rounded towards 0, equals 0 if [z] = 0)
- MOD_C(x, y, c): store [y] %  c  in [x] (equals 0 if  c  = 0, result is negative only if [y] < 0)
- MOD_R(x, y, z): store [y] % [z] in [x] (equals 0 if [z] = 0, result is negative only if [y] < 0)
- JEQ_C(x, c, i): jump to i if [x] = c
- JEQ_R(x, y, i): jump to i if [x] = [y]
- JNE_C(x, c, i): jump to i if [x] != c
- JNE_R(x, y, i): jump to i if [x] != [y]
- JLT_C(x, c, i): jump to i if [x] < c
- JLT_R(x, y, i): jump to i if [x] < [y]
- JLE_C(x, c, i): jump to i if [x] <= c
- JLE_R(x, y, i): jump to i if [x] <= [y]
- JGT_C(x, c, i): jump to i if [x] > c
- JGT_R(x, y, i): jump to i if [x] > [y]
- JGE_C(x, c, i): jump to i if [x] >= c
- JGE_R(x, y, i): jump to i if [x] >= [y]
```

The included example program is an implementation of [Bashicu Matrix System](https://kyodaisuu.github.io/basmat/definition.html).