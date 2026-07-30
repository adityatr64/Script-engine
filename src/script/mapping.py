# https://en.wikipedia.org/wiki/Help:IPA/English
# changing to phonemes for mapping

CONSONANT_KEYS = {
    'b', 'd', 'f', 'g', 'ɡ', 'h', 'ʤ', 'k', 'l', 'm', 'n', 'p', 'r', 's',
    't', 'v', 'w', 'z', 'ʒ', 'tʃ', 'ʧ', 'ʃ', 'θ', 'ð', 'ŋ', 'j',
    'bʰ', 'bh', 'tʃʰ', 'ʧʰ', 'chh', 'ɖ', 'dd', 'ɖʰ', 'ddh', 'ɽ',
    'ɡʰ', 'gʰ', 'gh', 'kʰ', 'kh', 'ɳ', 'nn', 'ʂ', 'sh', 'tʰ', 'tah', 'th'
}

VOWEL_KEYS = {
    'ə', 'e', 'ɛ', 'æ', 'ɪ', 'i', 'iː', 'ɒ', 'ɔ', 'o', 'ʊ', 'u', 'uː',
    'ʌ', 'ɑ', 'ɑː', 'aɪ', 'eɪ', 'ɔɪ', 'aʊ', 'oʊ', 'əʊ',
    'əm', 'am', 'əh', 'aha'
}

GLYPH_MAP = {
    # Special
    ' ': 'space',

    # Consonants
    'b': 'ba.svg',
    'd': 'da.svg',
    'f': 'fha.svg',
    'g': 'ga.svg',
    'ɡ': 'ga.svg',
    'h': 'ha.svg',
    'ʤ': 'ja.svg',
    'k': 'ka.svg',
    'l': 'la.svg',
    'm': 'ma.svg',
    'n': 'na.svg',
    'p': 'pa.svg',
    'r': 'ra.svg',
    's': 'sa.svg',
    't': 'ta.svg',
    'v': 'va.svg',
    'w': 'va.svg',
    'z': 'z.svg',
    'ʒ': 'jha.svg',
    'tʃ': 'cha.svg',
    'ʧ': 'cha.svg',
    'ʃ': 'shey.svg',
    'θ': 'ttha.svg',
    'ð': 'dha.svg',
    'ŋ': 'nga.svg',
    'j': 'ya.svg',

    # Aspirated & Retroflex Consonants
    'bʰ': 'bha.svg',
    'bh': 'bha.svg',
    'tʃʰ': 'chha.svg',
    'ʧʰ': 'chha.svg',
    'chh': 'chha.svg',
    'ɖ': 'dda.svg',
    'dd': 'dda.svg',
    'ɖʰ': 'ddha.svg',
    'ddh': 'ddha.svg',
    'ɽ': 'ddha.svg',
    'ɡʰ': 'gha.svg',
    'gʰ': 'gha.svg',
    'gh': 'gha.svg',
    'kʰ': 'kha.svg',
    'kh': 'kha.svg',
    'ɳ': 'nna.svg',
    'nn': 'nna.svg',
    'ʂ': 'sha.svg',
    'sh': 'sha.svg',
    'tʰ': 'tah.svg',
    'tah': 'tah.svg',
    'th': 'tha.svg',

    # Vowels
    'ə': 'a.svg',
    'e': 'e.svg',
    'ɛ': 'e.svg',
    'æ': 'ea.svg',
    'ɪ': 'i.svg',
    'i': 'ee.svg',
    'iː': 'ee.svg',
    'ɒ': 'o.svg',
    'ɔ': 'o.svg',
    'o': 'o.svg',
    'ʊ': 'u.svg',
    'u': 'uu.svg',
    'uː': 'uu.svg',
    'ʌ': 'a.svg',
    'ɑ': 'aa.svg',
    'ɑː': 'aa.svg',

    # Anusvara / Visarga & Nasals
    'əm': 'am.svg',
    'am': 'am.svg',
    'əh': 'aha.svg',
    'aha': 'aha.svg',

    # Diphthongs
    'aɪ': 'i.svg',
    'eɪ': 'e.svg',
    'ɔɪ': 'o.svg',
    'aʊ': 'aou.svg',
    'oʊ': 'o.svg',
    'əʊ': 'o.svg',
}

def get_glyph_filename(phoneme: str):
    return GLYPH_MAP.get(phoneme, None)

def is_consonant(phoneme: str) -> bool:
    return phoneme in CONSONANT_KEYS

def is_vowel(phoneme: str) -> bool:
    return phoneme in VOWEL_KEYS
