import click
import json
import os
import requests
import shutil
import time

from typing import Tuple
from time import sleep
from tqdm import tqdm

from bs4 import BeautifulSoup
from multiprocessing import Pool


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


def diceware(words: list) -> Tuple[list, list]:
    """
    Build the diceware list.
    """
    total_words = 7776
    results = []
    results_numbered = []

    # Remove duplicates
    words = list(set(words))

    with open('files/dicewarekit.txt', 'r') as file:
        for word in file:
            results.append(word.strip())

    if len(words) + len(results) < total_words:
        for word in words:
            results.append(word)
    else:
        for word in words:
            if len(results) < total_words:
                if len(word) > 3 and len(word) < 7:
                    if is_profanity_free(word):
                        results.append(word)

    results.sort()

    inc_p2 = inc_p3 = inc_p4 = inc_p5 = 1
    itr_p2 = itr_p3 = itr_p4 = itr_p5 = 0
    for index, word in enumerate(results):
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
        p2 = (itr_p2 % 6) + inc_p2 - itr_p2  # resets every 6^2 = 36
        p3 = (itr_p3 % 6**2) + inc_p3 - itr_p3  # resets every 6^3 = 216
        p4 = (itr_p4 % 6**3) + inc_p4 - itr_p4  # resets every 6^4 = 1296
        p5 = (itr_p5 % 6**4) + inc_p5 - itr_p5  # resets every 6^5 = 7776

        itr_p2 = itr_p2 + 1
        itr_p3 = itr_p3 + 1
        itr_p4 = itr_p4 + 1
        itr_p5 = itr_p5 + 1

        combinations = f'{p5}{p4}{p3}{p2}{p1}'
        results_numbered.append(f'{combinations}    {word}')

    return results, results_numbered


def is_profanity_free(word: str) -> bool:
    """
    Check for profanity.
    """
    profane_words = []
    clean = word not in profane_words
    return clean


def log(text: str, type: str = 'info') -> None:
    try:
        colors = {
            'success': 'green',
            'info': 'yellow',
            'warning': 'red'
        }

        click.secho(f'[{type}] - {text}', fg=colors[type])
    except KeyError as e:
        click.secho(f'Valid log types are: {", ".join(list(colors.keys()))}', fg='red')


def get_source(url: str) -> BeautifulSoup:
    """
    Get page source for the given url.
    """
    try:
        rs = requests.get(url)
    except requests.exceptions.MissingSchema as e:
        log(e, 'warning')
    else:
        source = BeautifulSoup(rs.content, 'html.parser')
        return source


def parse(source: BeautifulSoup) -> list:
    """
    Return a words list for the given page source.
    """
    children = source.find(id='lemmas').children
    words = []

    for node in children:
        dt = node.find('dt')

        if dt != -1:
            word = dt.find('b').text.strip(',')
            words.append(word)

    return words


def get_words(file_name: str) -> list:
    """
    Return words in a given file.
    """
    results = []

    if not os.path.isfile(file_name):
        return results

    with open(file_name, 'r') as words:
        for word in words:
            results.append(word.strip())

        words.close()

    return results


def create_output_dir() -> None:
    """
    Check if output directory exists.
    If not then create it.
    """
    if not os.path.isdir('output'):
        log('Output directory is missing. Creating directory...', 'warning')
        os.mkdir('output')


def clean_output_dir(is_clean: bool) -> None:
    """
    Delete output directory.
    """
    if os.path.isdir('output') and is_clean:
        shutil.rmtree('output')


def romanize_word(word: str = None) -> str:
    """
    Romanize a given word.
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
        'ϊ': 'i',
        'ΐ': 'i',
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
        'υ': 'y',
        'ύ': 'y',
        'ϋ': 'y',
        'ΰ': 'y',
        'φ': 'f',
        'χ': 'h',
        'x': 'h',
        'ψ': 'ps',
        'ω': 'o',
        'ώ': 'o',
    }
    if not word:
        return None

    chars = list(word.strip())
    result = []
    for char in chars:
        char = char.lower()
        result.append(mappings.get(char, char))

    return ''.join(result)


def export(file_name: str, words: list = None, file_type: str = 'txt') -> None:
    """
    Export a file.
    """
    if not words:
        log('Nothing to export', 'warning')
        return

    with open(f'output/{file_name}.{file_type}', 'w', encoding='utf-8') as output:
        if file_type == 'json':
            json.dump(words, output, ensure_ascii=False)
        else:
            for word in words:
                output.write(f'{word.strip()}\n')

        output.close()


def scrape(
    letter: str,
    pages: int,
    is_romanized: bool = False,
    is_json: bool = False,
    position: int = 0,
) -> None:
    """
    Scrapes www.greek-language.gr to build
    a full list of modern Greek words.

    https://www.greek-language.gr/greekLang/index.html
    """
    url = 'https://www.greek-language.gr/greekLang/modern_greek/tools/lexica/reverse/search.html'
    page = 0
    final_words = []
    final_words_romanized = []

    txt_output = open(f'output/{letter}.txt', 'a')
    existing_words = get_words(f'output/{letter}.txt')
    
    if is_romanized:
        romanized_output = open(f'output/{letter}_romanized.txt', 'a')
        existing_words_romanized = get_words(f'output/{letter}_romanized.txt')

    for page in tqdm(range(0, int(pages) + 10, 10), position=position, desc=letter, unit=" pages"):
        time.sleep(1)
        letter_url = f'{url}?start={page}&lq={letter}*'
        source = get_source(letter_url)
        words = parse(source)
        for word in words:
            # Append word to file only if it doesn't already exists
            if word not in existing_words:
                txt_output.write(f'{word.strip()}\n')
                final_words.append(word.strip())

            if is_romanized:
                # Append word to file only if it doesn't already exists
                if word not in existing_words_romanized:
                    word = romanize_word(word)
                    romanized_output.write(f'{word.strip()}\n')
                    final_words_romanized.append(word.strip())

    txt_output.close()

    if is_romanized:
        romanized_output.close()

    # Create json files
    if is_json:
        export(letter, final_words, 'json')

        if is_romanized:
            export(f'{letter}_romanized', final_words_romanized, 'json')


def fetch(
    letters: list,
    use_files: bool = False,
    is_romanized: bool = False,
    is_json: bool = False,
) -> None:
    if not use_files:
        log("Creating dictionary...", "info")
        pool = Pool()
        processes = []
        for idx, letter in enumerate(letters):
            try:
                pages = f'{letter["pages"]}'
                process = pool.apply_async(
                    scrape,
                    [
                        letter["letter"],
                        pages,
                        is_romanized,
                        is_json,
                        idx
                    ]
                )
                processes.append(process)
            except TypeError as e:
                log(e, 'warning')

        for process in processes:
            process.get()


def compile_dictionary(
    letters: list,
    is_romanized: bool = False,
    is_json: bool = False,
    is_diceware: bool = False,
) -> None:
    log("Compiling dictionary...", "info")
    final_words = []
    final_words_romanized = []
    
    for letter in tqdm(range(0, len(letters)), unit=" letters"):
        words = get_words(f'output/{letters[letter]["letter"]}.txt')
        for word in words:
            final_words.append(f'{word.strip()}')

            if is_romanized:
                word = romanize_word(word)
                final_words_romanized.append(f'{word.strip()}')

    export('index', final_words)

    if is_romanized:
        export('index', final_words_romanized)

    # Compile json files
    if is_json:
        log(f'Compiling json files...', 'info')
        export('index', final_words, 'json')

        if is_romanized:
            export('index_romanized', final_words_romanized, 'json')

    if is_diceware:
        log(f'Compiling diceware...', 'info')
        results, results_numbered = diceware(final_words)

        export('diceware', results)
        export('diceware_numbered', results_numbered)

        if is_romanized:
            romanized, romanized_numbered = diceware(final_words_romanized)

            export('diceware_romanized', romanized)
            export('diceware_romanized_numbered', romanized_numbered)

            if is_json:
                export('diceware_romanized', romanized, 'json')
                export('diceware_romanized_numbered', romanized_numbered, 'json')

        if is_json:
            export('diceware', results, 'json')
            export('diceware_numbered', results_numbered, 'json')
