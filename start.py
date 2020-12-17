import click
import requests
import sys
import time

from bs4 import BeautifulSoup

from utils import clean_output
from utils import compile_words
from utils import export
from utils import get_data
from utils import log
from utils import romanize_words


alphabet = [
    {
        'letter': 'Α',
        'pages': 31660
    },
    {
        'letter': 'Β',
        'pages': 5050
    },
    {
        'letter': 'Γ',
        'pages': 5890
    },
    {
        'letter': 'Δ',
        'pages': 7130
    },
    {
        'letter': 'Ε',
        'pages': 12530
    },
    {
        'letter': 'Ζ',
        'pages': 1500
    },
    {
        'letter': 'Η',
        'pages': 1310
    },
    {
        'letter': 'Θ',
        'pages': 2300
    },
    {
        'letter': 'Ι',
        'pages': 1720
    },
    {
        'letter': 'Κ',
        'pages': 17700
    },
    {
        'letter': 'Λ',
        'pages': 4740
    },
    {
        'letter': 'Μ',
        'pages': 13020
    },
    {
        'letter': 'Ν',
        'pages': 3790
    },
    {
        'letter': 'Ξ',
        'pages': 5250
    },
    {
        'letter': 'Ο',
        'pages': 4970
    },
    {
        'letter': 'Π',
        'pages': 18560
    },
    {
        'letter': 'Ρ',
        'pages': 2720
    },
    {
        'letter': 'Σ',
        'pages': 14340
    },
    {
        'letter': 'Τ',
        'pages': 7680
    },
    {
        'letter': 'Υ',
        'pages': 3170
    },
    {
        'letter': 'Φ',
        'pages': 5640
    },
    {
        'letter': 'Χ',
        'pages': 5370
    },
    {
        'letter': 'Ψ',
        'pages': 2080
    },
    {
        'letter': 'Ω',
        'pages': 470
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
    log(f'Getting letter {letter} words...', 'info')
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
    log(f'Got {letter} in {total}', 'success')
    return results


@click.command()
@click.option(
    '-l',
    '--letters',
    'has_letters',
    type=str,
    required=False,
    help='Get results for specified letter(s)'
)
@click.option(
    '-f',
    '--fresh',
    'is_fresh',
    is_flag=True,
    default=False,
    help='Fresh start'
)
@click.option(
    '-c',
    '--clean',
    'is_clean',
    is_flag=True,
    default=False,
    help='Clean output directory'
)
@click.option(
    '-r',
    '--romanize',
    'is_romanize',
    is_flag=True,
    default=False,
    help='Romazize words'
)
@click.option(
    '-j',
    '--json',
    'is_json',
    is_flag=True,
    default=False,
    help='Generate .json files'
)
def main(has_letters, is_fresh, is_clean, is_romanize, is_json):
    letters = alphabet

    if has_letters:
        letters = list(
            filter(lambda x: x['letter'] in has_letters.split(','), alphabet)
        )

    if is_clean:
        clean_output()

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

            results = romanize_words(data)
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
        results = romanize_words(results)
        export(file_name_romanized, results)

        if is_json:
            export(file_name_romanized, results, 'json')

    sys.exit(2)


if __name__ == '__main__':
    main()
