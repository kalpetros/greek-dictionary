# greek-dictionary

A utility to build a complete Greek dictionary.

**Note:**
Currently it only supports building an index.

# Getting started

### Install dependencies

Make sure [pipenv](https://pipenv.pypa.io/en/latest/) is installed.

```
$ python -m pipenv install
```

### Activate shell

```
$ python -m pipenv shell
```

### Build dictionary

```
$ python start.py [options]
```

### Options

| Option         | Type      | Description                                  |
| -------------- | --------- | ---------------------------------------------|
| -l, --letters  | string(s) | Get results for specified letter(s)          |
| -f, --files    |           | Use existing files to compile the dictionary |
| -r, --romanize |           | Romazize words                               |
| -j, --json     |           | Generate .json files                         |
| -d, --diceware |           | Generate diceware word list                  |

### Examples

To build a fresh dictionary:

```
$ python start.py
```

To build a dictionary for letter Ω:

```
$ python start.py -l Ω
```

To build a dictionary for letter Β and Ω:

```
$ python start.py -l Β,Ω
```
