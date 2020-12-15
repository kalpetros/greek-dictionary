import sys
import getopt

mappings = {
    'α': 'a',
    'ά': 'a',
    'β': 'v',
    'γ': 'g',
    'δ': 'd',
    'ε': 'e',
    'έ': 'e',
    'ζ': 'z',
    'η': 'h',
    'ή': 'h',
    'θ': 'th',
    'ι': 'i',
    'ί': 'i',
    'κ': 'k',
    'λ': 'l',
    'μ': 'm',
    'ν': 'n',
    'ξ': 'x',
    'ο': 'o',
    'ό': 'o',
    'π': 'p',
    'ρ': 'r',
    'σ': 's',
    'ς': 's',
    'τ': 't',
    'υ': 'y',
    'ύ': 'y',
    'φ': 'f',
    'χ': 'ch',
    'ψ': 'ps',
    'ω': 'o',
    'ώ': 'o'
}


def romanize(word):
    """
    Return romanized word
    """
    chars = list(word)
    result = []
    errors = []

    for char in chars:
        try:
            result.append(mappings[char.lower()])
        except Exception as e:
            errors.append(str(e))

    return ''.join(result)


def clean(min_length, max_length):
    """
    Remove duplicates
    """
    cleaned = []

    with open('output/compiled.txt', 'r') as file:
        for word in file:
            if len(word) > int(min_length) and len(word) < int(max_length):
                cleaned.append(word.strip())

    cleaned = set(cleaned)
    return cleaned


def main(argv):
    # Min word length
    min_length = 0
    # Max word length
    max_length = 1000

    try:
        opts, args = getopt.getopt(argv, "g:s:")
    except getopt.GetoptError:
        print('format.py -g <word_gt> -s <word_st>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-g'):
            min_length = arg
        elif opt in ('-s'):
            max_length = arg

    js = open('output/el.js', 'w')
    js.write('const el = [')
    js_r = open('output/el_romanized.js', 'w')
    js_r.write('const el = [')

    words = clean(min_length, max_length)
    for word in words:
        romanized = romanize(word)
        js_r.write(f'"{romanized}",\n')
        js.write(f'"{word}",\n')

    js.write('];')
    js.close()
    js_r.write('];')
    js_r.close()


if __name__ == '__main__':
    main(sys.argv[1:])
