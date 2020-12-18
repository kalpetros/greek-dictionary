import click
import os
import shutil
import requests
import sys
import time

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


def get_data(file_name):
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


def check():
    """
    Check if necessary files exist
    """
    if not os.path.isfile('files/el.txt'):
        log('el.txt is missing from files. Please restore the repository.', 'warning')
        sys.exit(2)

    if not os.path.isdir('output'):
        log('Output folder is missing. Creating folder...', 'warning')
        os.mkdir('output')


def clean_output():
    """
    Delete output files and folder
    """
    if not os.path.isdir('output'):
        log('Working directory already clean...', 'info')
        return

    shutil.rmtree('output')

    log('Working directory clean', 'success')

    return


def compile_words(letters):
    """
    Compile individual word files into one
    """
    log('Compiling files...', 'info')

    start = time.time()
    results = []

    for letter in letters:
        file_name = f'{letter["letter"]}.txt'

        words = get_data(f'output/{file_name}')
        for word in words:
            results.append(word)

    if not results:
        return results

    end = time.time()
    total = end - start

    log(f'Compiled in {total}', 'success')

    return results


def romanize_words(words):
    """
    Romanize words
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
    results = []

    if not words:
        log('No data provided', 'info')

        return results

    for word in words:
        result = []
        chars = list(word.strip())
        for char in chars:
            try:
                char = char.lower()
                result.append(mappings[char])
            except Exception as e:
                log(f'Could not map {str(e)}', 'warning')

        word = ''.join(result)
        results.append(word)

    log('Romanized all words', 'success')

    return results


def export(file_name, words, file_type='txt'):
    """
    Create a words file
    """
    if not words:
        log('No data provided', 'warning')
        return

    check()

    log(f'Creating file {file_name}.{file_type}...', 'info')

    output = open(f'output/{file_name}.{file_type}', 'w')

    if file_type == 'json':
        output.write('[')

    for word in words:
        if file_type == 'txt':
            output.write(f'{word.strip()}\n')
        elif file_type == 'json':
            output.write(f'"{word.strip()}",\n')

    if file_type == 'json':
        output.write(']')

    output.close()

    log(f'Created {file_name}.{file_type}', 'success')
