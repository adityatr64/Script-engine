import os
from .mapping import get_glyph_filename

GLYPH_DIR = '../glyphs'

def parse_shifted_text(text: str):
    glyph_paths = []
    
    for char in text:
        filename = get_glyph_filename(char)
        
        if filename == 'space':
            glyph_paths.append('SPACE') 
            continue
            
        if filename:
            path = os.path.join(GLYPH_DIR, filename)
            if os.path.exists(path):
                glyph_paths.append(path)
            else:
                print(f"not found: {filename}")
        else:
            pass
            
    return glyph_paths