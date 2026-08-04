> [!WARNING]
> **Note**: This README was written by AI.

# Script Engine

**Script Engine** translates English text into custom, handcrafted vector (SVG) script illustrations.

It converts input text into International Phonetic Alphabet (IPA) phonemes, maps consonants and vowels to custom 32×32 SVG glyphs with Indic-style top vowel stacking, and renders an organic handwritten connecting line and top vowel bars.

---

## Features

- **IPA Transliteration**: Automatically converts English text to IPA phonemes using `eng-to-ipa`.
- **Indic-style Vowel Stacking**: When vowels follow consonants, they are dynamically stacked above the preceding consonant.
- **Natural Handwriting Lines**: Dynamically generates smooth, organic handwritten squiggles for horizontal lines (`M ... C ...`).
- **Continuous Baseline**: Baseline consonant lines seamlessly connect across words.
- **Non-touching Top Vowel Lines**: Top vowel bars are inset so adjacent stacked vowels maintain visual separation.
- **100% Glyph Coverage**: Maps 45 custom vector glyphs across standard, aspirated, retroflex, nasal, and diphthong phonemes.

---

## Requirements

- **Python**: 3.10 or newer (cross-platform: Windows, macOS, Linux)
- **Dependencies**: Listed in `requirements.txt` (`eng-to-ipa`)

---

## Installation

```bash
git clone <repo-url>
cd Script-engine
python -m venv .venv

# On Windows PowerShell:
.\.venv\Scripts\Activate

# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Usage

### Desktop GUI Application (Python Tkinter)

Launch the native GUI application:

```bash
python gui.py
```

Features of the GUI:
- **Real-Time Input & IPA Display**: Instantly previews IPA phonemes as you type.
- **Interactive Vector Canvas**: Click and drag to pan, use mouse wheel to zoom vector graphics.
- **Live Parameter Controls**: Sliders for handwriting jitter, vowel stacking height, and top line insets.
- **Color & Theme Switching**: Customize stroke and canvas background colors; pick from 4 built-in preset themes (Dark Glass, Paper Light, Golden Ink, Neon Cyber).
- **Export & Phoneme Dictionary**: One-click SVG file export, copy SVG XML to clipboard, and inspect the 45-glyph IPA dictionary.

---

### CLI Command Options

Run the CLI entrypoint:

```bash
python src/main.py "the quick brown fox jumps over the lazy dog" -o output/illustration.svg
```

| Parameter | Type | Description | Default |
| --- | --- | --- | --- |
| `text` | Positional | Plain English string to render | *(Required)* |
| `-o`, `--output` | Flag | Output SVG file path | `output.svg` |

---

## Workflow Overview

1. **Phoneme Conversion** ([main.py](file:///e:/Script-engine/src/main.py)): Converts English text to IPA phonemes using `eng_to_ipa.convert()`.
2. **Parsing & Phoneme Matching** ([script/parser.py](file:///e:/Script-engine/src/script/parser.py)): Greedily matches IPA phonemes to glyph files in `src/glyphs/` via [script/mapping.py](file:///e:/Script-engine/src/script/mapping.py). Identifies baseline glyphs vs. attached stacked vowels.
3. **SVG Rendering & Handwriting Effect** ([render/svg.py](file:///e:/Script-engine/src/render/svg.py)): Merges glyph shapes, applies `translate(target_x, target_y)` for stacked vowels, and dynamically appends squiggly hand-drawn paths for top and baseline lines.

---

## Project Structure

```
Script-engine/
├── output/              # Generated SVG outputs (gitignored)
├── requirements.txt     # Python dependencies
├── README.md            # Documentation
└── src/
    ├── main.py          # CLI Entrypoint
    ├── glyphs/          # 45 SVG vector glyph assets
    ├── render/
    │   └── svg.py       # SVG composition & handwriting line generator
    └── script/
        ├── mapping.py   # IPA phonemes <-> SVG glyph mapping
        └── parser.py    # Text parsing & vowel stacking logic
```

---

## Customization

- **Glyph Vector Assets**: Custom SVG glyphs are stored in `src/glyphs/`. Each glyph is drawn on a `32×32` canvas.
- **Phoneme Mapping**: Edit `GLYPH_MAP` inside `src/script/mapping.py` to add new IPA symbols, adjust phoneme bindings, or modify special characters.
- **Rendering & Handwriting**: Adjust `stack_y_offset` (default `14.73`), `vowel_line_inset` (default `4`), or `jitter` inside `src/render/svg.py` to customize line offsets and handwritten squiggle intensity.
