#!/usr/bin/env python3
"""json_pretty.py – Tiny JSON pretty printer with optional colour.

Usage:
  json_pretty.py [-f FILE] [-c] [-s] [-i INDENT]
  cat data.json | json_pretty.py -c

Options:
  -f, --file   Path to JSON file (default: stdin)
  -c, --color  Colourise output
  -s, --sort   Sort object keys (default: True)
  -i, --indent Number of spaces for indentation (default: 2)
"""

import argparse
import json
import sys

# ANSI colour codes for basic JSON types
_COLOR_MAP = {
    str: "\033[32m",   # green
    int: "\033[33m",  # yellow
    float: "\033[33m",
    bool: "\033[35m", # magenta
    type(None): "\033[31m",  # red
}
RESET = "\033[0m"


def colourise(value: str, typ) -> str:
    """Wrap *value* in colour based on *typ* if colour is enabled."""
    colour = _COLOR_MAP.get(typ)
    return f"{colour}{value}{RESET}" if colour else value


def dump_pretty(data, indent: int, colour: bool, sort_keys: bool) -> str:
    """Return a pretty‑printed JSON string, colourising if requested."""
    if not colour:
        return json.dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

    # When colour is on we need to walk the structure manually
    def recurse(obj, level=0):
        sp = " " * (indent * level)
        if isinstance(obj, dict):
            items = []
            keys = sorted(obj) if sort_keys else list(obj)
            for k in keys:
                key_str = colourise(json.dumps(k), str)
                val_str = recurse(obj[k], level + 1)
                items.append(f"{sp}{' ' * indent}{key_str}: {val_str}")
            inner = ",\n".join(items)
            return f"{{\n{inner}\n{sp}}}"
        if isinstance(obj, list):
            elems = [recurse(e, level + 1) for e in obj]
            inner = ", ".join(elems)
            return f"[ {inner} ]"
        # Primitive types
        typ = type(obj)
        txt = json.dumps(obj, ensure_ascii=False)
        return colourise(txt, typ)

    return recurse(data)


def main():
    parser = argparse.ArgumentParser(description="Tiny JSON pretty printer")
    parser.add_argument("-f", "--file", type=argparse.FileType('r'), default=sys.stdin,
                        help="Path to JSON file (default: stdin)")
    parser.add_argument("-c", "--color", action="store_true", help="Colourise output")
    parser.add_argument("-s", "--sort", action="store_true", default=True,
                        help="Sort object keys (default: True)")
    parser.add_argument("-i", "--indent", type=int, default=2, help="Indent spaces (default: 2)")
    args = parser.parse_args()

    try:
        data = json.load(args.file)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Error parsing JSON: {e}\n")
        sys.exit(1)

    output = dump_pretty(data, indent=args.indent, colour=args.color, sort_keys=args.sort)
    print(output)


if __name__ == "__main__":
    main()
