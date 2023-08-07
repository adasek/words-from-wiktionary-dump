### Prerequisities
 1) python 3.10 or higher
 2) [poetry package manager](https://python-poetry.org/docs/)
 3) ICU library, e.g. package `libicu-dev` in Ubuntu

### Words from Wiktionary Dump
Experimental parser to load words from czech wiktionary

#### Running
Obtain latest `cs` dump from https://meta.wikimedia.org/wiki/Data_dumps / https://dumps.wikimedia.org/backup-index.html

```bash
poetry run python3 01_create-wordlist-from-wiktionary.py
# creates words, words_uniq, words_to_lemmas
```
