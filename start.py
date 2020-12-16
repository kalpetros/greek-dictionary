import getopt
import os
import requests
import shutil
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


def compile(letters):
    """
    Compile individual word files into one
    """
    output = open('output/el.txt', 'w')

    for letter in letters:
        with open(f'output/{letter["letter"]}.txt', 'r') as file:
            lines = file.readlines()

            for word in lines:
                output.write(f'{word.strip()}\n')

    output.close()


def scrape(letters):
    """
    Scrapes www.greek-language.gr to build
    a full list of modern Greek words

    https://www.greek-language.gr/greekLang/index.html
    """
    url = 'https://www.greek-language.gr/greekLang/modern_greek/tools/lexica/reverse/search.html'

    for letter in letters:
        start_time = time.time()
        output = open(f'output/{letter["letter"]}.txt', 'w')
        start = 0

        while start <= letter["pages"]:
            time.sleep(0.1)
            endpoint = f'{url}?start={start}&lq={letter["letter"]}*'
            start = start + 10
            source = get_source(endpoint)
            words = parse(source)
            for word in words:
                output.write(f'{word}\n')

        output.close()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f'{letter["letter"]} [DONE] [{elapsed_time}]')


def init():
    """
    Create output folder
    """
    print("Creating output folder...")
    if os.path.isdir('output'):
        shutil.rmtree('output')

    os.mkdir('output')


def main(argv):
    options = []

    try:
        opts, args = getopt.getopt(argv, "l:")
    except getopt.GetoptError:
        print('start.py -l <letter(s)>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-l'):
            options = arg.split(',')

    # Return user's matching letters from alphabet
    if not len(options):
        letters = alphabet
    else:
        letters = list(filter(lambda x: x['letter'] in options, alphabet))

    init()

    start_scraping = time.time()
    print("Getting words...")
    scrape(letters)
    end_scraping = time.time()
    total_scraping = end_scraping - start_scraping
    print(f'Total scraping time {total_scraping}')

    start_compilation = time.time()
    print("Compiling files...")
    compile(letters)
    end_compilation = time.time()
    total_compilation = end_compilation - start_compilation
    print(f'Finished in {total_compilation}')
    total_time = end_compilation - start_scraping
    print(f'Total time {total_time}')


if __name__ == '__main__':
    main(sys.argv[1:])
