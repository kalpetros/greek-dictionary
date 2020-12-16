import getopt
import os
import shutil
import sys

from utils import clean_duplicates
from utils import romanize


def main(argv):
    # Min word length
    min_length = 0
    # Max word length
    max_length = 1000

    if not os.path.isfile('files/el.txt'):
        print('el.txt is missing from files. Please restore the repository.')
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

    output_txt = open('output/el.txt', 'w')
    output_txt_romanized = open('output/el_romanized.txt', 'w')
    output_js = open('output/el.js', 'w')
    output_js_romanized = open('output/el_romanized.js', 'w')
    output_js.write('const el = [')
    output_js_romanized.write('const el = [')
    words = []

    if not os.path.isfile('output/compiled.txt'):
        print('compiled.txt is missing. Copying from files...')
        shutil.copy('files/el.txt', 'output/compiled.txt')

    with open('output/compiled.txt', 'r') as file:
        for word in file:
            words.append(word.strip())

    words = clean_duplicates(min_length, max_length, words)
    words.sort()

    for word in words:
        romanized = romanize(word)
        output_txt.write(f'{word}\n')
        output_txt_romanized.write(f'{romanized}\n')
        output_js.write(f'"{word}",\n')
        output_js_romanized.write(f'"{romanized}",\n')

    output_js.write('];')
    output_js_romanized.write('];')

    output_txt.close()
    output_txt_romanized.close()
    output_js.close()
    output_js_romanized.close()


if __name__ == '__main__':
    main(sys.argv[1:])
