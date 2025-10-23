# GoogolScript

Welcome to GoogolScript (GS for short), my own programming language.

The desire to create my own language is relatively new to me. The idea came to me only after I ran into some minor aesthetic issues with my usual programming language of choice - Python.

To explain, I am a googologist, which is a person who studies large numbers, fast-growing functions, ordinal notations, and other related topics. In short, it's a personal hobby of mine. And, being a mathematical topic, it requires its concepts to be formalized - either through mathematical notation when we're talking about purely abstract concepts, or through direct implementation in some programming language when we're talking about algorithms. Most googologists choose Python, me included.

Python is easy to learn, easy to use, and fairly powerful. However, over the years, I've run into some issues with it. For example, its syntax isn't as flexible as I'd like it to be. If it could be more like Coq, that would be great. It can also be a bit verbose. In this regard, if it could be more like JavaScript, that would also be great.

And so, having the appropriate knowledge after years of studying mathematics and computer science, I've decided to try and create my own language.

See below regarding instructions for what is already implemented, as well as a list of planned features.

## Instructions

For now, only a REPL that echoes literals is implemented. To run it, run googolscript.py.

For documentation, simply read the source code, it's fairly basic for now.

## Planned features

### Basics

* Name: GoogolScript
* File extension: .gs, .gsc
* Implementation: tree-walk interpreter in Python + Lark, will eventually be ported to Rust
* Encoding: Assumes UTF-8 for source files, supports all combinations of LF, CR, LFCR, CRLF for newlines
* .gs comes with standard library included ("std" or maybe "gs"), .gsc (GoogolScript Core) doesn't - it comes without any pre-defined sugar
* Alphabet: The language syntax supports only printable ASCII, newline (any mixture of LF and CR) and tab; comments and strings can use any Unicode characters

### Philosophy

* JavaScript-like syntax but more modern and intelligent like Python
* Will offer plenty of syntactic shorthands
* Multi-paradigm: imperative, objective, functional
* Clarity and explicit behavior preferred over implicit or hidden actions
* Newlines and spaces can often be omitted, it should be possible to write the entire program on one line
* Not designed for raw speed; expressiveness and ease of writing is the priority
* Avoids runtime error handling, exceptions must be handled explicitly
* Capable of introspection and defining custom syntax
* Default behavior can be modified using built-in flags
* The design should allow for growth: richer types, new control structures, domain-specific notations

### Comments

* End-of-line: //
* End-of-scope: ///
* Block: /* ... */ (can nest)
* Description: //* ... *// (can nest; turns into metadata for the subsequent statement or block)

### Scopes

* Denoted with braces: { ... }
* Can be named too, in which case they will turn into a namespace (everything in it is still public and normally executed)

### Separators

* Semicolons and newlines separate statements (they are not needed to terminate them)
* Commas are used to separate e.g. function arguments, container items, and arithmetic expressions (comma operator)
* Possible extension: semicolons inside arrays or function arguments may serve as an alternative separator to allow comma as operator

### Identifiers

* Alphanumeric characters + underscore, case-sensitive, cannot start with a number
* Underscore acts as a throwaway variable

#### Naming conventions:

* Lowercase = variables and functions
* Capitalized = types and classes
* Uppercase = built-in constants

### Variables and Bindings

* Binding the return value of a block is allowed
* Shadowing is allowed
* Referencing a name before it's initialized is an error
* Decide what these mean, decide if needed at all: (none), let, def, var, val, mut
* Possible to declare without initialization (no default value): "let x"
* * := --- new binding with shadowing
* * <- --- value update (variable must exist)
* * =  --- equivalent to <- if name exists, otherwise :=
* Type inference and explicit typing both supported ("type name" and "name : type" both supported)
* Assignments can be chained

### Memory management

* := always creates a new copy
* $x = y --- defines an alias (reference)
* In arguments:
* * x --- make a copy and pass
* * $x --- make an alias and pass
* assign by value/reference
* compare by value/reference

### Booleans and logic

* Literals: TRUE, FALSE
* No truthy/falsy values, everything is explicit
* Operators (can do short-circuiting): !, &, |, => (this is also their precedence)
* Comparison (always by value): ==, <, >, <=, >=, !=, !<, !>, !<=, !>=
* "=" is equivalent to one of :=, <-, == depending on context
* Comparison between values of different types is allowed and always returns FALSE

### Null

* Literal: NULL
* Essentially a singleton type
* Some built-in functions/operations may return it by default
* Null coalescing: x ?? y is equivalent to "x if x is not null else y" (in Pythonic terms)
* Decide if it should be internal only (meaning assignment/passing isn't allowed) or work the same as user-defined singletons

### Strings

* Denoted via double quotes only: "..."
* Full unicode support via \u escapes; if the character is printable, it can also be written literally
* Escape sequences: `\\`, `\"`, `\n`, `\t`, `\u{int}`, `\{`, `\}`
* Interpolation: "{expr}"
* Mutable, essentially dynamic arrays of chars, many of the same array operations apply
* Lexicographic comparison

#### Built-in methods

(non-exhaustive list, names aren't final, some may be replaced by exclusive syntax)

* length
* upper, lower, title, capitalize, flipcase
* trim, trim_left, trim_right
* find, index, count, has
* startswith, endswith
* insert, replace
* split, join
* substring, substring_rev
* is_alpha, is_digit, is_numeric, is_whitespace
* is_upper, is_lower
* center, ljust, rjust, zfill
* concat, repeat

### Numbers

* "int" only, includes infinity (INF)
* Optional sign: + or - (works with INF too)
* Base range: 2 to 64
* General base form: `<base>b<digits>`
* Apostrophes are ignored inside numbers, e.g. 1'000'000
* Allowed digits by base:
* * up to base 10: 0-9
* * up to base 36: 0-9A-Z or 0-9a-z
* * up to base 62: 0-9A-Za-z
* * up to base 64: 0-9A-Za-z$_
* Higher bases with structured digits (list form) via `Int(base=..., value=[...])`
* Operators: +, -, *, /, %
* Multi-infix comparisons are allowed (e.g., a < b < c)

### Control Flow

* Execution is sequential: the program moves statement by statement, entering blocks/scopes as they appear
* Keywords: if, else, elif, loop, exit, next
* Ternary operator: "cond ? x : y"
* Pattern matching (will be fleshed out later)

#### If/else:

* if cond { ... } ...
* ... elif cond { ... } ...
* ... else { ... }
* can have a return value

#### Loops:

* The body may be a single statement or a block
* loop { ... } (infinite loop)
* loop num { ... } (executes num times; num may be an int or an immutable expression that evaluates to int)
* loop cond { ... } (while loop)
* can have a return value
* loop control: exit, next, exit(int), next(int), exit(label), next(label)
* decide how to implement loop labels
* possible shortform loop syntax using @
* Python's for-loops are rather categorized as comprehensions

### Functions

* "fn name(args) body" or "name = args -> body"
* Body may be a block { ... } or a single expression
* Rich argument syntax like in Python / Lisp
* Arguments are pass-by-copy by default
* First-class, passing or returning a function creates a closure (decide how it's gonna behave exactly)
* "x <- y" can be used as "nonlocal x = y" if x doesn't exist in the function's scope; = is always :=
* Last statement is an implicit return; return can also be forced explicitly via "return" or "<-"
* Functions that don't return anything (procedures) do NOT implicitly return a NULL
* Functions can return structured argument packs (positional and keyword) and callers may destructure or ignore parts of the return
* Custom operators and mixfix functions can be defined
* Consider "space operator" for calling, i.e. x y as an alternative to x(y)

### Types
* Fundamental built-in types: Int, Bool, Text, Null, Func, Array, Table, Code
* Type annotations are optional and inferred
* * Either "Type name" or "name : Type"
* * For functions: "Type -> Type"
* * The type of the function argument list is a tuple
* Advanced: parametric types, sum/union types, traits/interfaces and generics with constraints
* "a : b" == "type(a) is b"
* no type declared in argument == any type expected

### Containers

* Two primary dynamic composite types: Array and Table
* Arrays and Tables support rich operations and methods; specialized variants (tuples, sets, tensors) are planned as part of the composite datatype system
* Type system will allow fine-grained constraints (const size, non-repeating, ordering, homogeneity)
* Strings are arrays of characters, with the same indexing and slicing operations
* Methods like length, slice, concat, repeat apply equally to strings and arrays
* Special properties: non-repeating values, hypercuboid shape, ordering, tagging
* Special combinations: strings "ab", tuples (a,b), sets {a,b}, tensors `[a;b]`, `[a,,b]`

#### Array

* Ordered, indexable sequence of values
* Literal syntax: [a, b, c]
* Indexing and slicing: arr(i), arr(i:j), arr(i:j:k)
* All indices optional: arr(:), arr(:j), arr(i:), arr(::k)
* Indexes are 0-based
* Negative indexes count from the end
* Out-of-bounds indexing raises an error
* Concatenation: arr1 + arr2
* Repetition: arr * n
* Methods (non-exhaustive): length, push, pop, insert, remove, slice, reverse, sort, map, filter, reduce

#### Table:

* Key/value mapping
* Literal syntax: { key1: val1, key2: val2 }
* Keys may be strings, numbers, or any immutable value
* Lookup: tbl(key)
* Update/insert: tbl(key) <- val
* Methods (non-exhaustive): length, keys, values, has, remove, merge, map, filter

#### Variability:

* Fixed-length arrays vs dynamic arrays
* Homogeneous arrays vs heterogeneous arrays
* Const tables vs mutable tables

#### Kinds:
* Tuple (mutable nothing)
* Mutable tuple (mutable value)
* Fixed list (mutable value and type)
* Typed list (mutable value and size)
* Generic list (mutable value, type and size)

### Modules, Imports, and Exports

* Imports are only allowed at top level
* Nothing is exported by default unless marked
* A module's canonical name is its normalized file path without extension
* The ".gs" extension is implied and omitted in import strings
* Mark definitions for export with "export" (functions/types/classes/constants only)
* dot syntax for importing only specific things from a file, curly braces like in Rust for importing multiple things

### Generators

### Comprehensions

### Reductions

### Enhanced for-loops

### I/O

* Text by default, UTF-8. Binary modes are available via open()
* File handles are auto-closed at end of the scope where they were created; explicit close() is also available
* stdin, stdout, stderr
* print: writes stringified items to stdout separated by spaces, ending with newline
* eprint: writes to stderr
* input: reads a line (without trailing newline) from stdin

### File Read/Write

* read: reads entire file as UTF-8 text
* write_text: overwrites file with stringified items concatenated
* append_text
* read_all
* read_bytes
* write_bytes

### Path Utilities

* exists, is_file, is_dir
* mkdir
* remove
* rename
* listdir

### File Methods

* file.write()
* file.write_line()
* file.read_all()
* file.read_line()
* file.read_bytes()
* file.flush(), file.seek(), file.tell(), file.close()

### I/O

* print()
* input()
* append(filename, ...) - appends to file, or creates a new one if it doesn't exist yet
* overwrite(filename, ...) - explicitly overwrites a file with new data, or creates a new one if it doesn't exist yet
* overwrite(filename, start, ...) - starts overwriting at a given position
* x=read(filename) - reads whole file
* x=load(filename) - loads a file such that array-like shenanigans can be performed with it
* store(filename) - explicitly closes the file after load() opened it
* not necessary, files will be automatically closed after the scope in which they have been opened is left

### Classes and objects:

* I'm still contemplating doing this on a prototype basis like in Javascript, since it seems really powerful and generic
* there will be generics too
* Static vs. dynamic, encapsulation, type, prototyping, method & class sugar, inheritance, polymorphism, abstract, mixin, generics

### Inductive types

### Metaprogramming
* you can define something with the Code type and the expression won't be evaluated, instead it will be converted to the AST
* you can then use various normal ways for extracting info out of this structure or modifying it (basically you can treat it as some very complex type and then do the same magic to it as you can do to custom types in Ocaml/Coq)
* custom operations, relations, modify existing definitions, etc
* define a piece of code without evaluating it using ::=, e.g. x ::= 3+5 will yield the AST of 3+5
* another way to do that would be to surround the code in question with `` (figure out how to make this syntax recursive, similar to nested comments)
* .identifier == access properties of the interpreter