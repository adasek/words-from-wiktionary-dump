from pathlib import Path
import pickle
from collections import Counter


# Read wordlist created by 01-parse-wiktionary.py
wordlist = set()
with open('words_uniq') as wordlist_file:
    for word in wordlist_file.readlines():
        wordlist.add(word.strip().lower())

print(len(wordlist))

# Load the corpus (sentences) created by 02-read-books.py
def load_sentence_corpus(pickle_file_path: Path):
    with open(pickle_file_path, 'rb') as infile:
        corpus: Counter = pickle.load(infile)
    return corpus

sentences = load_sentence_corpus("out/sentences-42142039.pickle")

print(sentences.total())
