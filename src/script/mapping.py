# https://en.wikipedia.org/wiki/Help:IPA/English
# changing to phonemes for mapping
'''
CONSONANTS = 
    'b': 'ब', 'd': 'ड', 'f': 'फ़', 'g': 'ग', 'h': 'ह', 'ʤ': 'ज', 'k': 'क', 
    'l': 'ल', 'm': 'म', 'n': 'न', 'p': 'प', 'r': 'र', 's': 'स', 't': 'ट', 
    'v': 'व', 'w': 'व', 'z': 'ज़', 'ʒ': 'झ़', 'tʃ': 'च', 'ʃ': 'श', 'θ': 'थ', 
    'ð': 'द', 'ŋ': 'ङ', 'j': 'य', 'ɡ': 'ग' # ɡ is a variant of g

VOWELS =
    'ə': ('अ', ''),     'e': ('ए', 'े'),     'æ': ('ऐ', 'ै'), 
    'ɪ': ('इ', 'ि'),    'i': ('ई', 'ी'),     'iː': ('ई', 'ी'),
    'ɒ': ('ऑ', 'ॉ'),    'ɔ': ('ऑ', 'ॉ'),     'ʊ': ('उ', 'ु'), 
    'u': ('ऊ', 'ू'),    'uː': ('ऊ', 'ू'),    'ʌ': ('अ', ''), 
    'ɑ': ('आ', 'ा'),    'ɑː': ('आ', 'ा'),
    
    # Diphthongs (Gliding vowels)
    'aɪ': ('आइ', 'ाइ'), 'eɪ': ('एइ', 'ेइ'),  'ɔɪ': ('ऑइ', 'ॉइ'),
    'aʊ': ('आउ', 'ाउ'), 'oʊ': ('ओ', 'ो'),    'əʊ': ('ओ', 'ो')

'''
VOWELS={
    'ɑ':'a.svg',
    'ɔ':'o.svg',
    'o':'o,svg',
    'æ':'i.svg',
    'aɪ':'i.svg'
    


}

CONSONANTS = {
    ' ': 'space',    'b': 'ba.svg',    'd': 'da.svg',
    'ʤ': 'ja.svg',    'ð': 'dha.svg',    'f': 'fha.svg',
    'g': 'ga.svg',    'h': 'ha.svg',    'w':'va.svg',#hw also
    'j':'ya.svg',    'k':'ka.svg',    'l':'la.svg',
    'm':'ma.svg',    'n':'na.svg',    'ŋ':'nga.svg',
    'p':'pa.svg',    'r':'ra.svg',    's':'sa.svg',
    'ʃ':'shey.svg',#श
    't':'ta.svg',    'ʧ':'cha.svg',    'θ':'ttha.svg',
    'v':'va.svg',    'z':'z.svg',    'ʒ':'jha.svg',
}

def get_glyph_filename(char: str):
    return GLYPH_MAP.get(char, None)