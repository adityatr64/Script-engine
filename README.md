# Script Engine

English text --> custom glyph-based SVG. This script engine ingests a string, shifts it with a Caesar cipher, maps each character to a handcrafted glyph, and stitches the glyph SVGs into a single, continuous line illustration.

## Requirements
- Python 3.10 or newer (tested on Windows PowerShell, works cross-platform)
- Glyph SVG assets placed under `src/glyphs/` with names that match `src/script/mapping.py`
- Write access to `output/` (or whichever path you target) for final SVG export

## Installation
```pwsh
git clone <repo-url>
cd "Script engine"
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
```

## Usage
Run the CLI entrypoint with the text you want to convert:

```pwsh
cd src
python main.py "hello world" -o ..\output\trial.svg
```

Command-line options:

| Flag | Description | Default |
| --- | --- | --- |
| positional `text` | Plain English string to render | required |
| `-o`, `--output` | Destination SVG path | `output.svg` (written relative to `pwd`) |

Workflow overview:
1. **Transform** – `transform/caesar.py` shifts characters by +4 and normalizes to lowercase.
2. **Parse** – `script/parser.py` resolves each shifted character to an SVG filename via `script/mapping.py` and validates that the file exists under `src/glyphs/`.
3. **Render** – `render/svg.py` merges the glyph SVG fragments into a single document, inserting `SPACE` gaps where needed and writing the final file.

Outputs land in whichever path you pass to `-o`. The provided `output/` folder is ignored by Git so you can keep generated art separate from source.

## Customization
- **Glyphs**: Drop or update SVG files under `src/glyphs/`. Keep each glyph 32×32 for seamless joins, or adjust `GLYPH_SIZE` in `render/svg.py` if you prefer a different canvas.
- **Character map**: Edit `GLYPH_MAP` inside `src/script/mapping.py` to remap characters, add punctuation, or tweak space handling.
- **Cipher**: Change the shift value (default `4`) or swap in a different transform by editing `transform/caesar.py` and updating `src/main.py` accordingly.

## Project Structure
```
src/
	main.py           # CLI entrypoint
	glyphs/           # Individual glyph SVG assets
	render/svg.py     # SVG merger
	script/
		mapping.py      # Character -- > glyph lookup
		parser.py       # Resolves glyph paths
	transform/
		caesar.py       # Text normalization & shift
output/             # Generated SVGs (gitignored)
```

## Roadmap Ideas
Not much planned for future mostly a custom tool for my book

Contributions welcome—open an issue or PR with your proposal before diving in.
