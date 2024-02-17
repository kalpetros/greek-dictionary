import click
import json
import os
import requests
import shutil
import time

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


def diceware(words):
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
                    if is_clean(word):
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


def is_clean(word):
    """
    Check for profanity.
    """
    clean = True
    profane_words = []

    if word in profane_words:
        clean = False

    return clean


def log(text, type):
    colors = {
        'success': 'green',
        'info': 'yellow',
        'warning': 'red'
    }

    click.secho(f'[{type}] - {text}', fg=colors[type])


def get_source(url):
    """
    Get page source for the given url.
    """
    rs = requests.get(url)
    source = BeautifulSoup(rs.content, 'html.parser')

    return source


def parse(source):
    """
    Return words array for the given page source.
    """
    children = source.find(id='lemmas').children
    words = []

    for node in children:
        dt = node.find('dt')

        if dt != -1:
            word = dt.find('b').text.strip(',')
            words.append(word)

    return words


def scrape(
    letter: str,
    pages: int,
    is_romanized: bool = False,
    is_json: bool = False,
    position: int = 0,
):
    """
    Scrapes www.greek-language.gr to build
    a full list of modern Greek words.

    https://www.greek-language.gr/greekLang/index.html
    """
    url = 'https://www.greek-language.gr/greekLang/modern_greek/tools/lexica/reverse/search.html'
    page = 0
    existing_words = []
    existing_words_romanized = []
    final_words = []
    final_words_romanized = []

    txt_output = open(f'output/{letter}.txt', 'a')

    try:
        with open(f'output/{letter}.txt') as file:
            existing_words = [word.strip() for word in file]
            file.close()
    except Exception:
        pass
    
    if is_romanized:
        romanized_output = open(f'output/{letter}_romanized.txt', 'a')
        try:
            with open(f'output/{letter}_romanized.txt') as file:
                existing_words_romanized = [word.strip() for word in file]
                file.close()
        except Exception:
            pass

    for page in tqdm(range(0, int(pages) + 10, 10), position=position, desc=letter, unit=" pages"):
        time.sleep(0.1)
        letter_url = f'{url}?start={page}&lq={letter}*'
        source = get_source(letter_url)
        words = parse(source)
        for word in words:
            if word not in existing_words:
                txt_output.write(f'{word.strip()}\n')
                final_words.append(word.strip())

            if is_romanized:
                if word not in existing_words_romanized:
                    word = romanize_word(word)
                    romanized_output.write(f'{word.strip()}\n')
                    final_words_romanized.append(word.strip())

    txt_output.close()

    if is_romanized:
        romanized_output.close()

    # Create json files
    if is_json:
        with open(f'output/{letter}.json', 'w', encoding='utf-8') as json_file:
            json.dump(final_words, json_file, ensure_ascii=False)
            json_file.close()
        
        if is_romanized:
            with open(f'output/{letter}_romanized.json', 'w', encoding='utf-8') as json_file:
                json.dump(final_words_romanized, json_file, ensure_ascii=False)
                json_file.close()


def get_words(file_name) -> list:
    """
    Return words in a given file.
    """
    results = []

    if not os.path.isfile(file_name):
        return results

    try:
        with open(file_name, 'r') as words:
            for word in words:
                results.append(word.strip())
    except Exception as e:
        log(f'Could not get data {str(e)}', 'warning')

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
    if not os.path.isdir('output'):
        return

    if is_clean:
        shutil.rmtree('output')

    return


def romanize_word(word: str = None) -> str:
    """
    Romanize word
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
        try:
            char = char.lower()
            result.append(mappings.get(char, char))
        except Exception as e:
            log(f'Could not map {str(e)}', 'warning')

    word = ''.join(result)
    return word


def export(file_name, words, file_type='txt') -> None:
    """
    Create a words file.
    """
    if not words:
        log('No data to export', 'warning')
        return

    with open(f'output/{file_name}.{file_type}', 'w', encoding='utf-8') as output:
        if file_type == 'json':
            json.dump(words, output, ensure_ascii=False)
        else:
            for word in words:
                output.write(f'{word.strip()}\n')

        output.close()


def fetch(
        use_files: bool,
        is_romanized: bool,
        is_json: bool,
        letters: list
) -> None:
    if not use_files:
        log("Creating dictionary...", "info")
        pool = Pool()
        processes = []
        for idx, letter in enumerate(letters):
            pages = f'{letter["pages"]}'
            process = pool.apply_async(
                scrape, [letter["letter"], pages, is_romanized, is_json, idx]
            )
            processes.append(process)

        for process in processes:
            process.get()


def compile_dictionary(
        is_romanized: bool,
        is_json: bool,
        is_diceware: bool,
        letters: list
) -> None:
    log("Compiling dictionary...", "info")
    final_words = []
    final_words_romanized = []
    compiled_index = open('output/index.txt', 'w')
    if is_romanized:
        compiled_index_romanized = open(f'output/index_romanized.txt', 'a')
    
    for letter in tqdm(range(0, len(letters)), unit=" letters"):
        words = get_words(f'output/{letters[letter]["letter"]}.txt')
        for word in words:
            compiled_index.write(f'{word.strip()}\n')
            final_words.append(f'{word.strip()}')

            if is_romanized:
                word = romanize_word(word)
                compiled_index_romanized.write(f'{word.strip()}\n')
                final_words_romanized.append(f'{word.strip()}')

    compiled_index.close()
    if is_romanized:
        compiled_index_romanized.close()

    # Compile json files
    if is_json:
        log(f'Compiling json files...', 'info')
        with open(f'output/index.json', 'w', encoding='utf-8') as json_file:
            json.dump(final_words, json_file, ensure_ascii=False)
            json_file.close()
        
        if is_romanized:
            with open(f'output/index_romanized.json', 'w', encoding='utf-8') as json_file:
                json.dump(final_words_romanized, json_file, ensure_ascii=False)
                json_file.close()

    if is_diceware:
        log(f'Compiling diceware...', 'info')
        results, results_numbered = diceware(final_words)

        if is_romanized:
            romanized, romanized_numbered = diceware(final_words_romanized)

            export('diceware_romanized', romanized)
            export('diceware_romanized_numbered', romanized_numbered)

            if is_json:
                export('diceware_romanized', romanized, 'json')
                export('diceware_romanized_numbered', romanized_numbered, 'json')

        export('diceware', results)
        export('diceware_numbered', results_numbered)

        if is_json:
            export('diceware', results, 'json')
            export('diceware_numbered', results_numbered, 'json')
