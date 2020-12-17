import click
import os
import shutil
import sys
import time


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
    Check if el.txt file exists
    """
    if not os.path.isfile('files/el.txt'):
        log('el.txt is missing from files. Please restore the repository.', 'warning')
        sys.exit(2)

    if not os.path.isdir('output'):
        log('Output folder is missing. Creating folder...', 'warning')
        os.mkdir('output')


def clean_output():
    """
    Remove output files and folder
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

    end = time.time()
    total = end - start

    log(f'Compiled in {total}', 'success')

    return results


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
    Create a file with words
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


def log(text, type):
    colors = {
        'success': 'green',
        'info': 'yellow',
        'warning': 'red'
    }

    click.secho(f'[{type}] - {text}', fg=colors[type])
