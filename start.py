import getopt
import requests
import sys
import time

from bs4 import BeautifulSoup

from utils import clean
from utils import compile_words
from utils import export
from utils import get_data
from utils import romanize


alphabet = [
    {
        'letter': 'Χ',
        'pages': 20
    },
    {
        'letter': 'Ψ',
        'pages': 20
    },
    {
        'letter': 'Ω',
        'pages': 70
    }
]


def get_source(url):
    """
    Get page source for the given url
    """
    rs = requests.get(url)
    source = BeautifulSoup(rs.content, 'html.parser')

    return source


def parse(source):
    """
    Return words array for the given page source
    """
    children = source.find(id='lemmas').children
    words = []

    for node in children:
        dt = node.find('dt')

        if dt != -1:
            word = dt.find('b').text.strip(',')
            words.append(word)

    return words


def scrape(letter: str, pages: int):
    """
    Scrapes www.greek-language.gr to build
    a full list of modern Greek words

    https://www.greek-language.gr/greekLang/index.html
    """
    print(f'[INFO] - Getting letter {letter} words...')
    start = time.time()
    url = 'https://www.greek-language.gr/greekLang/modern_greek/tools/lexica/reverse/search.html'
    results = []
    page = 0

    while page <= int(pages):
        time.sleep(0.1)
        endpoint = f'{url}?start={page}&lq={letter}*'
        source = get_source(endpoint)
        words = parse(source)
        page = page + 10
        for word in words:
            results.append(word)

    end = time.time()
    total = end - start
    print(f'[SUCCESS] - Got {letter} in {total}')
    return results


def main(argv):
    letters = alphabet
    is_clean = False
    is_fresh = False
    is_json = False
    is_romanize = False

    try:
        opts, args = getopt.getopt(
            argv, "l:fcrj", ['length', 'fresh', 'clean', 'romanize', 'json']
        )
    except getopt.GetoptError:
        print('start.py -l <letter(s)> -f -c -r -j')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-l', '--length'):
            letters = list(
                filter(lambda x: x['letter'] in arg.split(','), alphabet)
            )
        elif opt in ('-f', '--fresh'):
            is_fresh = True
        elif opt in ('-c', '--clean'):
            is_clean = True
        elif opt in ('-r', '--romanize'):
            is_romanize = True
        elif opt in ('-j', '--json'):
            is_json = True

    if is_clean:
        clean()

        if not is_fresh and not is_romanize and not is_json:
            sys.exit(2)

    for letter in letters:
        file_name = f'{letter["letter"]}'
        pages = f'{letter["pages"]}'
        data = get_data(f'output/{file_name}.txt')
        # Run only if user wants to update the words
        if is_fresh:
            data = scrape(file_name, pages)
            export(file_name, data)

        if is_romanize:
            file_name_romanized = f'{file_name}_romanized'

            results = romanize(data)
            export(file_name_romanized, results)

            if is_json:
                export(file_name_romanized, results, 'json')

        if is_json:
            export(file_name, data, 'json')

    results = compile_words(letters)
    export('el', results)

    if is_json:
        export('el', results, 'json')

    if is_romanize:
        file_name_romanized = 'el_romanized'
        results = romanize(results)
        export(file_name_romanized, results)

        if is_json:
            export(file_name_romanized, results, 'json')

    sys.exit(2)


if __name__ == '__main__':
    main(sys.argv[1:])
