# Bean

Bean is a high-level programming language based on various high-level languages such as Python, JavaScript and OCaml, and designed primarily with aesthetics in mind.

The name is a reference to Lean, a particularly elegant proof assistant, and to Mr. Bean, whose comedy transcends language.

The current version of the project resides in the Bean folder. The other folders will be slowly phased out.

## Planned Features

### Naming Conventions
* AaaBbb: types, classes
* aaa_bbb: variables, functions
* AAA_BBB: constants

### Basic Types
* Int (later implementations may include infinity; rational numbers might be implemented as a library)
* Bool
* Str (no Char)
* Errors lie outside of the type system (meaning they need not be specified in type signatures), but can still be manipulated like normal types

### Basic Functions

#### Integer Operations
* add(Int, Int): adds two ints
* sub(Int, Int): subtracts two ints
* mul(Int, Int): multiplies two ints
* div(Int, Int): divides two ints, returns the whole number part; div(Int, 0) returns Error 
* mod(Int, Int): divides two ints, returns the remainder (constraints have yet to be determined)

* Int -> Int: neg, abs, sign
* Int × Int -> Int: cmp_sign, pow, root, root_rem, log, log_rem, gcd, lcm, clamp, min, max
* Int × Int -> Bool: eq, neq, lt, leq, gt, geq, is_div, in_range
* Int × Str -> chr
* Bool -> Bool: not
* Bool × Bool -> Bool: and, or, impl, eq, neq
* Str -> Int: len, ord
* Str -> Bool: is_digit, is_letter, is_alpha, is_space, is_lower, is_upper, is_int, is_int_base, is_bool, is_ascii, is_ascii_printable
* Str -> Str: rev, lower, upper, capital, trim, trim_left, trim_right
* Str × Int -> Str: rep, get, slice_from, slice_to, pad_left, pad_right
* Str × Int × Int -> Str: slice, pad
* Str × Str -> Int: cat, count, count_overlap, find_first, find_last
* Str × Str -> Bool: is_prefix, is_suffix, has, is_subseq, eq, neq, lt, leq, gt, geq
* Str × Str -> Str: replace, replace_first, replace_last

to_int, to_int_base, to_bool
* Polymorphic: if, if_cmp, type, to_str, apply, parse
* Error handling: try (includes fallback), catch, raise, finally