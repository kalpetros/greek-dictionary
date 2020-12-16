import os
import sys
import shutil
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


def generate_diceware():
    """
    Generate diceware list
    """
    if os.path.isdir('tmp'):
        shutil.rmtree('tmp')

    os.mkdir('tmp')

    template = open('tmp/init.txt', 'w')
    output = open('output/el_diceware.txt', 'w')
    js = open('output/el_diceware.js', 'w')
    words = []

    with open('files/dicewarekit.txt', 'r') as file:
        for word in file:
            template.write(f'{word.strip()}\n')

    with open('output/el_romanized.txt', 'r') as file:
        for word in file:
            template.write(f'{word.strip()}\n')

    template.close()

    with open('tmp/init.txt', 'r') as file:
        for word in file:
            words.append(word.strip())

    words.sort()

    js.write('const el = [')

    inc_p2 = inc_p3 = inc_p4 = inc_p5 = 1
    itr_p2 = itr_p3 = itr_p4 = itr_p5 = 0
    for index, word in enumerate(words):
        if itr_p2 % 6 == 0:
            inc_p2 = inc_p2 + 6 + 1

        if itr_p3 % 6**2 == 0:
            inc_p3 = inc_p3 + 6**2 + 1

        if itr_p4 % 6**3 == 0:
            inc_p4 = inc_p4 + 6**3 + 1

        if itr_p5 % 6**4 == 0:
            inc_p5 = inc_p5 + 6**4 + 1

        if (itr_p2 % 6**2 == 0):
            itr_p2 = 0
            inc_p2 = 1

        if (itr_p3 % 6**3 == 0):
            itr_p3 = 0
            inc_p3 = 1

        if (itr_p4 % 6**4 == 0):
            itr_p4 = 0
            inc_p4 = 1

        if (itr_p5 % 6**5 == 0):
            itr_p5 = 0
            inc_p5 = 1

        p1 = index % 6 + 1  # resets every 6
        p2 = (itr_p2 % 6) + inc_p2 - itr_p2  # reset every 6^2 = 36
        p3 = (itr_p3 % 6**2) + inc_p3 - itr_p3  # resets every 6^3 = 216
        p4 = (itr_p4 % 6**3) + inc_p4 - itr_p4  # resets every 6^4 = 1296
        p5 = (itr_p5 % 6**4) + inc_p5 - itr_p5  # resets every 6^5 = 7776

        test = f'{p5}{p4}{p3}{p2}{p1}'
        output.write(f'{test}    {word}\n')
        js.write(f'"{word}",\n')

        itr_p2 = itr_p2 + 1
        itr_p3 = itr_p3 + 1
        itr_p4 = itr_p4 + 1
        itr_p5 = itr_p5 + 1

    output.close()
    js.write('];')
    js.close()
    shutil.rmtree('tmp')


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

    if not os.path.isfile('output/compiled.txt'):
        print('compiled.txt is missing. Copying from files...')
        shutil.copy('files/compiled.txt', 'output/compiled.txt')

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

    if not os.path.isfile('files/compiled.txt'):
        print('compiled.txt is missing from files. Please restore the repository.')
        sys.exit(2)

    if not os.path.isdir('output'):
        print('Output folder is missing. Creating folder...')
        os.mkdir('output')

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

    el = open('output/el.txt', 'w')
    el_r = open('output/el_romanized.txt', 'w')
    js = open('output/el.js', 'w')
    js.write('const el = [')
    js_r = open('output/el_romanized.js', 'w')
    js_r.write('const el = [')

    words = clean(min_length, max_length)
    for word in words:
        romanized = romanize(word)
        el.write(f'{word}\n')
        el_r.write(f'{romanized}\n')
        js_r.write(f'"{romanized}",\n')
        js.write(f'"{word}",\n')

    el.close()
    el_r.close()
    js.write('];')
    js.close()
    js_r.write('];')
    js_r.close()

    generate_diceware()


if __name__ == '__main__':
    # main(sys.argv[1:])
    generate_diceware()
