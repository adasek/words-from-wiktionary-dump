### Words from Wiktionary Dump
Experimental parser to load words from czech wiktionary


#### Running
Obtain latest `cs` dump from https://meta.wikimedia.org/wiki/Data_dumps / https://dumps.wikimedia.org/backup-index.html

```bash
poetry run python3 01_create-wordlist-from-wiktionary.py > ./words
sort ./words|uniq > ./words_uniq 
```
