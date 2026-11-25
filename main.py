#!/usr/bin/env python3
"""Write the one word this entry would delete from the dictionary.

The competition asks for a single word, nothing else attached, written
to entry.txt. The chosen word is "irregardless": a word that is not a
word at all, yet somehow keeps showing up in the dictionary anyway.
Deleting it costs the language nothing and saves everyone the argument.
"""

import argparse
import os
import sys

WORD = "irregardless"
MAX_CHARS = 77


def gate_ok(text):
    """Return True when text passes the competition gate."""
    if not isinstance(text, str):
        return False
    if not (1 <= len(text) <= MAX_CHARS):
        return False
    if text.strip() == "":
        return False
    return text.split() == [text] and len(text.split()) == 1


def write_entry(path):
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(WORD)


def read_back(path):
    with open(path, "r", encoding="utf-8", newline="") as handle:
        return handle.read()


def self_test():
    failures = []
    if WORD != "irregardless":
        failures.append("word mismatch")
    if len(WORD) != 12:
        failures.append("word is not 12 characters")
    if not gate_ok(WORD):
        failures.append("gate rejects the word")
    if gate_ok(""):
        failures.append("gate accepts empty text")
    if gate_ok("two words"):
        failures.append("gate accepts two words")
    if gate_ok("x" * 78):
        failures.append("gate accepts 78 characters")
    if gate_ok("   "):
        failures.append("gate accepts whitespace only")
    if failures:
        for failure in failures:
            print("FAIL: " + failure, file=sys.stderr)
        return 1
    print("self-test OK: %r is one word, %d chars" % (WORD, len(WORD)))
    return 0


def check():
    if not gate_ok(WORD):
        print("FAIL: entry word fails the gate", file=sys.stderr)
        return 1
    print("check OK: %r passes the gate (1 word, %d chars, max %d)"
          % (WORD, len(WORD), MAX_CHARS))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Write the word to delete from the dictionary.")
    parser.add_argument("--check", action="store_true",
                        help="validate the entry without writing it")
    parser.add_argument("--self-test", action="store_true",
                        help="run internal validation checks")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    if args.check:
        return check()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    path = os.path.join(out_dir, "entry.txt")
    write_entry(path)
    written = read_back(path)
    raw = open(path, "rb").read()
    if raw != WORD.encode("utf-8"):
        print("FAIL: entry.txt bytes do not match the entry word",
              file=sys.stderr)
        return 1
    if written != WORD:
        print("FAIL: entry.txt does not match the entry word",
              file=sys.stderr)
        return 1
    if not gate_ok(written):
        print("FAIL: written entry.txt fails the gate", file=sys.stderr)
        return 1
    print("wrote %s (%d chars)" % (path, len(written)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
