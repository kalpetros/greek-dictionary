# greek-dictionary

A utility to build a complete Greek dictionary

# Getting started

```
$ python start.py [options]
```

### Options

| Option         | Type      | Description                         |
| -------------- | --------- | ----------------------------------- |
| -l, --length   | String(s) | Get results for specified letter(s) |
| -f, --fresh    |           | Fresh start                         |
| -c, --clean    |           | Clean output directory              |
| -r, --romanize |           | Romazize words                      |
| -j, --json     |           | Generate .json files                |

### Examples

To build a fresh dictionary:

```
$ python start.py -f -r -j
```

To build a dictionary for letter Ω:

```
$ python start.py -l Ω -f -r -j
```

To build a dictionary for letter Β and Ω:

```
$ python start.py -l Β,Ω -f -r -j
```
