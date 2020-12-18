import click
import sys

from utils import alphabet
from utils import clean_output
from utils import compile_words
from utils import export
from utils import get_data
from utils import log
from utils import romanize_words
from utils import scrape

from diceware import diceware


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
@click.option(
    '-d',
    '--diceware',
    'is_diceware',
    is_flag=True,
    default=False,
    help='Generate diceware files'
)
def main(has_letters, is_fresh, is_clean, is_romanize, is_json, is_diceware):
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

    if is_diceware:
        results, results_numbered = diceware(results)
        export('el_diceware', results)
        export('el_diceware_numbered', results_numbered)

        if is_json:
            export('el_diceware', results, 'json')
            export('el_diceware_numbered', results_numbered, 'json')

    sys.exit(2)


if __name__ == '__main__':
    main()
