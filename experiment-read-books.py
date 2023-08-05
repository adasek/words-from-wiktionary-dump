from pathlib import Path
from nltk.tokenize import wordpunct_tokenize, sent_tokenize
from collections import Counter
import pickle

# Words taken from wiktionary
# versus
# words found in an e-book

# Load the word list
# created by the run.py

wordlist = set()
with open('words_uniq') as wordlist_file:
    for word in wordlist_file.readlines():
        wordlist.add(word.strip().lower())

print(len(wordlist))

book_paths = Path('ebooks').rglob('*.txt')

def is_alfanumeric(word: str) -> bool:
    return not any(not c.isalnum() for c in word.strip())

def save_result(corpus: dict):
    print()
    print(corpus.total())
    with open(f"out/corpus-{corpus.total()}.pickle", 'wb') as outputfile:
        pickle.dump(corpus, outputfile)

# word -> occurrences
corpus = Counter()

for i, book_path in enumerate(book_paths):
    try:
        with open(book_path) as book_file:
            for line in book_file.readlines():
                corpus.update([word for word in wordpunct_tokenize(line) if is_alfanumeric(word)])
        print(".", end="", flush=True)
    except UnicodeDecodeError:
        print("!", end="", flush=True)
    # if i % 1000 == 0:
        # save_result(corpus)
save_result(corpus)
print(corpus.most_common(100))
# unknown_words = book_wordlist - wordlist

# print(sorted(list(unknown_words), key=len, reverse=True))
# unknown_percentage = 100 * len(unknown_words) / len(book_wordlist)
# print(f"Unknown percentage: {round(unknown_percentage, 2)}%")
# print(f"Unknown words: {len(unknown_words)}")

