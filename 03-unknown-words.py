from pathlib import Path
import pickle
from collections import Counter

def is_alfanumeric(word: str) -> bool:
    return not any(not c.isalnum() for c in word.strip())


# Read wordlist created by 01-create-wordlist-from-wiktionary
wiktionary_wordlist = set()
with open('words_uniq') as wordlist_file:
    for word in wordlist_file.readlines():
        wiktionary_wordlist.add(word.strip().lower())

print(len(wiktionary_wordlist))

# Load the corpus (words) created by 02-read-books.py
def load_counter_pickle(file_path: Path):
    with open(file_path, 'rb') as infile:
        corpus: Counter = pickle.load(infile)
    return corpus

words_counter = load_counter_pickle("corpus/word_counter.pickle")

print(words_counter.total())

unknown_words_counter = {key: words_counter[key] for key in words_counter.keys() if key not in wiktionary_wordlist}

filtered_words_counter = {word.lower(): count for word, count in unknown_words_counter.items() if is_alfanumeric(word) and len(word) > 1 and count > 10}
unknown_words = sorted(filtered_words_counter.items(), key=lambda x: x[1])

print(unknown_words)
print("----")
unknown_percentage = 100 * len(unknown_words) / len(words_counter.keys())
print(f"Unknown percentage: {round(unknown_percentage, 2)}%")
print(f"Unknown words: {len(unknown_words)}")

