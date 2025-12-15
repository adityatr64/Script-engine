def shift_text(text: str, shift: int = 4) -> str:
    """
    Shifts english characters by `shift` amount.
    Example: 'a' (shift 4) -> 'e'
    """
    result = []
    for char in text:
        if char.isalpha():
            start = 65 if char.isupper() else 97
            shifted_char = chr((ord(char) - start + shift) % 26 + start)
            result.append(shifted_char)
        else:
            result.append(char)
    
    return "".join(result).lower()