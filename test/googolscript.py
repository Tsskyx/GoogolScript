#!/usr/bin/env python3
"""
Toy language skeleton
---------------------
A minimal, structured starting point for your programming language implementation.
- Reads a source file into memory (UTF-8 by default).
- Defines a lexer interface (Protocol) and a Token type.
- Wires the call-site where the lexer would be invoked (implementation left to you).

Usage:
  python toy_language_skeleton.py path/to/source.tl --encoding utf-8
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Optional, Protocol
import argparse
import sys

# -----------------------------
# Token & Lexer interface
# -----------------------------

@dataclass(frozen=True)
class Token:
    """Simple token placeholder. Extend as needed.

    kind: A short label like 'IDENT', 'NUMBER', 'GT', ...
    lexeme: The exact substring from the source.
    line/column: 1-based positions (optional but handy for diagnostics).
    """
    kind: str
    lexeme: str
    line: int
    column: int

class Lexer(Protocol):
    """Interface for your lexer.

    Implement this in your own module/class. The `lex` method should yield
    `Token` objects scanned from the provided source text.
    """
    def lex(self, source: str) -> Iterable[Token]:
        ...  # TODO: implement in your lexer

# -----------------------------
# Language driver (very small)
# -----------------------------

class ToyLanguage:
    def __init__(self) -> None:
        self.source: Optional[str] = None
        self.tokens: list[Token] = []

    def load_source(self, path: Path, *, encoding: str = "utf-8") -> None:
        """Read entire file into memory.

        If you later want a streaming/buffered approach, replace this method or
        add an alternate code-path.
        """
        try:
            self.source = path.read_text(encoding=encoding)
        except UnicodeDecodeError as e:
            raise SystemExit(f"Decoding error while reading {path}: {e}")
        except OSError as e:
            raise SystemExit(f"I/O error while reading {path}: {e}")

    def run_lexer(self, lexer: Lexer) -> None:
        """Invoke the provided lexer implementation on self.source.

        The lexer is expected to be implemented by you. This method only wires
        the call and collects tokens into a list for now.
        """
        if self.source is None:
            raise RuntimeError("Source not loaded; call load_source() first.")
        # Convert any iterable to a list so we can inspect/print later.
        self.tokens = list(lexer.lex(self.source))

    def dump_tokens(self, out: Optional[Iterator[str]] = None) -> None:
        """Utility: print tokens (debug only)."""
        sink = out if out is not None else sys.stdout
        for t in self.tokens:
            print(f"{t.kind}\t{t.lexeme!r}\t@{t.line}:{t.column}", file=sink)  # type: ignore[arg-type]

# -----------------------------
# CLI
# -----------------------------

def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Toy language skeleton")
    p.add_argument("source", type=Path, help="path to source file")
    p.add_argument(
        "--encoding",
        default="utf-8",
        help="text encoding to use when reading the source (default: utf-8)",
    )
    p.add_argument(
        "--dump-tokens",
        action="store_true",
        help="after lexing, print tokens (for debugging)",
    )
    return p


def main(argv: Optional[list[str]] = None) -> int:
    args = build_arg_parser().parse_args(argv)

    lang = ToyLanguage()
    lang.load_source(args.source, encoding=args.encoding)

    # --- Lexer hook -------------------------------------------------------
    # Replace `YourLexer()` with your actual implementation that conforms
    # to the `Lexer` Protocol above. For example:
    #
    #   from my_lexer import MyLexer
    #   lexer: Lexer = MyLexer()
    #
    # For now, we provide a stub that raises if accidentally used.
    class _UnimplementedLexer:
        def lex(self, source: str) -> Iterable[Token]:  # type: ignore[override]
            raise NotImplementedError(
                "No lexer provided. Implement Lexer.lex(source) and plug it in."
            )

    lexer: Lexer = _UnimplementedLexer()  # TODO: replace with your lexer instance
    # ---------------------------------------------------------------------

    # If you want to postpone plugging in a real lexer, you can comment out the
    # next two lines. Keeping them in ensures the wiring is correct.
    try:
        lang.run_lexer(lexer)
    except NotImplementedError as e:
        print(e, file=sys.stderr)
        return 2

    if args.dump_tokens:
        lang.dump_tokens()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
