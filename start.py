import click
import sys
import json
import os

from multiprocessing import Pool

from diceware import diceware

from utils import alphabet
from utils import clean_output
from utils import export
from utils import get_words
from utils import log
from utils import scrape
from utils import romanize_word
from utils import create_output_dir
from tqdm import tqdm

@click.command()
@click.option(
    '-l',
    '--letters',
    'has_letters',
    type=str,
    help='Get results for specified letter(s)'
)
@click.option(
    '-f',
    '--files',
    'use_files',
    is_flag=True,
    default=False,
    help='Use existing files to compile a dictionary'
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
    '--romanized',
    'is_romanized',
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
@click.option(
    '-d',
    '--diceware',
    'is_diceware',
    is_flag=True,
    default=False,
    help='Generate diceware files'
)
def main(has_letters, use_files, is_clean, is_romanized, is_json, is_diceware):
    letters = alphabet
    pool = Pool()

    if has_letters:
        letters = list(
            filter(lambda x: x['letter'] in has_letters.split(','), alphabet)
        )

    if use_files and is_clean:
        log("You cannot use clean and files options together", "warning")
        sys.exit(2)

    # Delete folders and files
    if is_clean:
        clean_output()

    if not os.path.isdir('output'):
        create_output_dir()

    # Begin data scraping
    processes = []
    if not use_files:
        log("Creating dictionary...", "info")
        for idx, letter in enumerate(letters):
            pages = f'{letter["pages"]}'
            process = pool.apply_async(
                scrape, [letter["letter"], pages, is_romanized, is_json, idx]
            )
            processes.append(process)

    for process in processes:
        process.get()

    # Compile dictionary
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

    sys.exit(2)


if __name__ == '__main__':
    main()
