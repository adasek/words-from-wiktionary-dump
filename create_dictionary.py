from collections import Counter
from helper import load_counter_pickle
import random

def starts_with_lowercase(word: str) -> str:
    if len(word) == 0:
        return False
    return word[0].islower()

def contains_trailing_hyphen(word: str):
    return word.endswith('-') or word.endswith('\xad') or word.endswith('\u00ad') or word.endswith('\N{SOFT HYPHEN}')

def soft_normalize_word(word: str) -> str:
    word = word.strip().strip('.… ')
    word = word.replace('\xad', '')
    word = word.replace('\u00ad', '')
    word = word.replace('\N{SOFT HYPHEN}', '')
    return word

# Read wordlist created by 01-create-wordlist-from-wiktionary
wiktionary_words = set()
with open('words_uniq') as wordlist_file:
    for word in wordlist_file.readlines():
        if starts_with_lowercase(word.strip()):
            wiktionary_words.add(soft_normalize_word(word.strip()))

print(len(wiktionary_words))


corpus_words_counter = load_counter_pickle("corpus/word_counter3.pickle")
corpus_words = set()
for word, occurrences in corpus_words_counter.items():
    if occurrences > 5 and starts_with_lowercase(word) and not contains_trailing_hyphen(word):
        corpus_words.add(soft_normalize_word(word))

words = corpus_words.union(wiktionary_words)

print(len(words))

# print(random.sample(list(words), 1000))

print(random.sample(list(corpus_words), 1000))
