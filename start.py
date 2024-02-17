import click
import os
import sys

from utils import alphabet
from utils import clean_output_dir
from utils import log
from utils import fetch
from utils import create_output_dir
from utils import compile_dictionary


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
def main(has_letters, use_files, is_clean, is_romanized, is_json, is_diceware) -> None:
    letters = alphabet
    if has_letters:
        letters = list(
            filter(lambda x: x['letter'] in has_letters.split(','), alphabet)
        )

    if use_files and is_clean:
        log("You cannot use clean and files options together", "warning")
        sys.exit(2)

    clean_output_dir(is_clean)
    create_output_dir()
    fetch(use_files, is_romanized, is_json, letters)
    compile_dictionary(is_romanized, is_json, is_diceware, letters)
    sys.exit(2)


if __name__ == '__main__':
    main()
