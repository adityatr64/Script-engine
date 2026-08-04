import sys
import os

# Ensure src directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import eng_to_ipa as p
from script.parser import parse_ipa_text
from render.svg import merge_svgs
from script.mapping import GLYPH_MAP

def generate_script(text: str, options: dict = None) -> dict:
    """
    Translates English text into custom Script Engine SVG.
    
    Options dict can contain:
    - output_path (str, optional)
    - jitter (float, default 0.5)
    - stack_y_offset (float, default 15.02167)
    - vowel_line_inset (float, default 4.0)
    - stroke_color (str, default "#000000")
    - bg_color (str, default None)
    
    Returns dict:
    {
        "input_text": str,
        "ipa_text": str,
        "glyph_items": list,
        "svg_content": str,
        "output_path": str or None,
        "glyph_count": int,
    }
    """
    if options is None:
        options = {}
        
    text = text.strip() if text else ""
    if not text:
        return {
            "input_text": "",
            "ipa_text": "",
            "glyph_items": [],
            "svg_content": "",
            "output_path": None,
            "glyph_count": 0,
            "error": "Empty input text"
        }
        
    # Convert English text line by line to preserve explicit newlines
    lines = text.splitlines()
    ipa_lines = [p.convert(line) for line in lines]
    ipa_text = "\n".join(ipa_lines)
    
    # Parse IPA text to glyph items
    glyph_items = parse_ipa_text(ipa_text)
    
    if not glyph_items:
        return {
            "input_text": text,
            "ipa_text": ipa_text,
            "glyph_items": [],
            "svg_content": "",
            "output_path": None,
            "glyph_count": 0,
            "error": "No valid glyphs found to render"
        }
        
    jitter = options.get("jitter", 0.5)
    stack_y_offset = options.get("stack_y_offset", 14.73)
    vowel_line_inset = options.get("vowel_line_inset", 4.0)
    max_line_width = options.get("max_line_width", 500.0)
    line_spacing = options.get("line_spacing", 56.0)
    output_path = options.get("output_path", None)
    
    svg_content = merge_svgs(
        glyph_items=glyph_items,
        output_path=output_path,
        stack_y_offset=stack_y_offset,
        vowel_line_inset=vowel_line_inset,
        jitter=jitter,
        max_line_width=max_line_width,
        line_spacing=line_spacing
    )
    
    return {
        "input_text": text,
        "ipa_text": ipa_text,
        "glyph_items": glyph_items,
        "svg_content": svg_content,
        "output_path": output_path,
        "glyph_count": len([item for item in glyph_items if item != 'SPACE']),
        "error": None
    }

def get_glyph_dictionary() -> dict:
    """Returns mapping dictionary of IPA phonemes to glyph SVG filenames."""
    return GLYPH_MAP
