import os
from .mapping import GLYPH_MAP, get_glyph_filename, is_consonant, is_vowel

GLYPH_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'glyphs'))

def parse_ipa_text(ipa_text: str):
    """
    Parses an IPA string into a list of glyph descriptors using greedy phoneme matching.
    Each item is either 'SPACE' or dict {'path': str, 'is_attached': bool}.
    """
    clean_ipa = ipa_text.replace("ˈ", "").replace("ˌ", "").replace("*", "")
    sorted_phonemes = sorted(GLYPH_MAP.keys(), key=len, reverse=True)
    
    items = []
    i = 0
    prev_was_consonant = False
    
    while i < len(clean_ipa):
        match = None
        for phoneme in sorted_phonemes:
            if clean_ipa.startswith(phoneme, i):
                match = phoneme
                break
        
        if match:
            filename = get_glyph_filename(match)
            if filename == 'space':
                items.append('SPACE')
                prev_was_consonant = False
            elif filename:
                path = os.path.join(GLYPH_DIR, filename)
                if os.path.exists(path):
                    if is_vowel(match) and prev_was_consonant:
                        items.append({'path': path, 'is_attached': True})
                        prev_was_consonant = False
                    else:
                        is_cons = is_consonant(match)
                        items.append({'path': path, 'is_attached': False})
                        prev_was_consonant = is_cons
                else:
                    print(f"Glyph file not found: {filename}")
            i += len(match)
        else:
            i += 1
            
    return items
