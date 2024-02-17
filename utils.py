import click
import os
import requests
import shutil
import sys
import time
import json
from time import sleep
from tqdm import tqdm

from bs4 import BeautifulSoup


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


def is_clean(word):
    """
    Check for profanity
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


def scrape(
    letter: str,
    pages: int,
    is_romanized: bool = False,
    is_json: bool = False,
    position: int = 0,
):
    """
    Scrapes www.greek-language.gr to build
    a full list of modern Greek words

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
    Return words in a given file
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


def create_output_dir():
    """
    Check if output directory exists.
    If not then create it.
    """
    if not os.path.isdir('output'):
        log('Output directory is missing. Creating directory...', 'warning')
        os.mkdir('output')


def clean_output() -> None:
    """
    Delete output files and folder
    """
    if not os.path.isdir('output'):
        return

    shutil.rmtree('output')
    return


def romanize_word(word=None):
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


def export(file_name, words, file_type='txt'):
    """
    Create a words file
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
