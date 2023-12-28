from pathlib import Path
import pickle
from collections import Counter


def is_alfanumeric(word: str) -> bool:
    return not any(not c.isalnum() for c in word.strip())


def norm(word: str) -> str:
    return word.lower().strip()


def starts_with_lowercase(word: str) -> str:
    return word[0].islower()


# Read wordlist created by 01-create-wordlist-from-wiktionary
wiktionary_wordlist = set()
with open('words_uniq') as wordlist_file:
    for word in wordlist_file.readlines():
        wiktionary_wordlist.add(norm(word))

print(len(wiktionary_wordlist))


# Load the corpus (words) created by 02-read-books.py
def load_counter_pickle(file_path: Path):
    with open(file_path, 'rb') as infile:
        corpus: Counter = pickle.load(infile)
    return corpus


coprus_words_counter = load_counter_pickle("corpus/word_counter.pickle")

# Avoiding all names (starting with capital letter)
unknown_words_counter = {norm(word): coprus_words_counter[word] for word in coprus_words_counter.keys() if
                         norm(word) not in wiktionary_wordlist and starts_with_lowercase(word)}

filtered_words_counter = {word: count for word, count in unknown_words_counter.items() if
                          is_alfanumeric(word) and len(word) > 1 and count > 0}
unknown_words_with_count = sorted(filtered_words_counter.items(), key=lambda x: x[1])
unknown_words = set(map(lambda x: x[0], unknown_words_with_count))

for word_with_count in unknown_words_with_count:
    print(word_with_count[0], word_with_count[1])
print("----")
# absolute number of unknown words
unknown_words_count = sum(filtered_words_counter.values())
total_words_count = sum(coprus_words_counter.values())
total_unknown_percentage = 100 * unknown_words_count / total_words_count

unknown_percentage = 100 * len(unknown_words) / len(coprus_words_counter.keys())
print(f"Unknown percentage: {round(unknown_percentage, 2)}% (per-word)")
print(f"Total unknown percentage: {round(total_unknown_percentage, 2)}% ({unknown_words_count} out of {total_words_count})")
print(f"Unknown words: {len(unknown_words)}")
