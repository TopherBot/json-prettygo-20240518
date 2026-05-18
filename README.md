# json-prettygo-20240518

A **tiny** Python utility that formats JSON in a human‑readable way.

## Features
- Reads JSON from **stdin** or a file argument.
- Outputs indented, sorted JSON.
- Optional colourised output using ANSI escape codes.
- Zero‑dependency (standard library only).

## Installation & Usage
```bash
# Clone (or just copy the single file)
git clone https://github.com/yourname/json-prettygo-20240518.git
cd json-prettygo-20240518

# Make it executable (optional)
chmod +x json_pretty.py

# Run on a file
./json_pretty.py data.json

# Pipe from another command
cat data.json | ./json_pretty.py -c   # colourised output
```

## Options
| Flag | Description |
|------|-------------|
| `-f`, `--file` | Path to JSON file (default: read from stdin) |
| `-c`, `--color`| Colourise the output (default: off) |
| `-s`, `--sort` | Sort object keys alphabetically (default: on) |
| `-i`, `--indent` | Number of spaces for indentation (default: 2) |

## License
MIT – see the repository for details.
