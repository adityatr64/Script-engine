# temporary until i add syllabel based mapping
GLYPH_MAP = {
    'a': 'a.svg',
    'b': 'ba.svg',
    'c': 'cha.svg',
    'd': 'da.svg',
    'e': 'e.svg',
    'f': 'fha.svg',
    'g': 'ga.svg',
    'h': 'ha.svg',
    'i': 'i.svg',
    'j': 'ja.svg',
    'k': 'ka.svg',
    'l': 'la.svg',
    'm': 'ma.svg',
    'n': 'na.svg',
    'o': 'o.svg',
    'p': 'pa.svg',
    'q': 'ka.svg', 
    'r': 'ra.svg',
    's': 'sa.svg',
    't': 'ta.svg',
    'u': 'u.svg',
    'v': 'va.svg',
    'w': 'va.svg',
    'x': 'k.svg', 
    'y': 'ya.svg',
    'z': 'z.svg',
    ' ': 'space',
}

def get_glyph_filename(char: str):
    return GLYPH_MAP.get(char, None)