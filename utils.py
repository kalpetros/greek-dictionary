def clean_profanity(words):
    """
    Remove profanity
    """
    results = []

    for word in words:
        results.append(word)

    return results


def clean_duplicates(min_length, max_length, words):
    """
    Remove duplicates
    """
    cleaned = []

    for word in words:
        if len(word) > int(min_length) and len(word) < int(max_length):
            cleaned.append(word.strip())

    cleaned = list(set(cleaned))

    return cleaned


def romanize(word):
    """
    Return romanized word
    """
    mappings = {
        'α': 'a',
        'ά': 'a',
        'β': 'v',
        'γ': 'g',
        'δ': 'd',
        'ε': 'e',
        'έ': 'e',
        'ζ': 'z',
        'η': 'i',
        'ή': 'i',
        'θ': 'th',
        'ι': 'i',
        'ί': 'i',
        'κ': 'k',
        'λ': 'l',
        'μ': 'm',
        'ν': 'n',
        'ξ': 'ks',
        'ο': 'o',
        'ό': 'o',
        'π': 'p',
        'ρ': 'r',
        'σ': 's',
        'ς': 's',
        'τ': 't',
        'υ': 'u',
        'ύ': 'u',
        'φ': 'f',
        'χ': 'h',
        'ψ': 'ps',
        'ω': 'o',
        'ώ': 'o'
    }

    chars = list(word)
    result = []
    errors = []

    for char in chars:
        try:
            result.append(mappings[char.lower()])
        except Exception as e:
            errors.append(str(e))

    return ''.join(result)
