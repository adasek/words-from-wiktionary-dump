from pathlib import Path
import pickle
import math
from collections import Counter


# Load the corpus (words) created by 02-read-books.py
def load_counter_pickle(file_path: Path):
    with open(file_path, 'rb') as infile:
        corpus: Counter = pickle.load(infile)
    return corpus

def normalize_word(w):
    for char in [*" \u200c –'…"]:
        w = w.strip(char)
    return w.lower()

def is_alfanumeric(word: str) -> bool:
    return not any(not c.isalnum() for c in word.strip())



def save_result(corpus: dict, pickle_filename:Path):
    with open(pickle_filename, 'wb') as outputfile:
        pickle.dump(corpus, outputfile)


def counter_reduce(list):
    if len(list) == 1:
        return list[0]
    elif len(list) == 0:
        return Counter()
    return counter_reduce(list[0:math.floor(len(list)/2)]) + counter_reduce(list[math.floor(len(list)/2):])
