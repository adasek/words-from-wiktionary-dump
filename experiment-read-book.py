from pathlib import Path
from nltk.tokenize import wordpunct_tokenize

# Words taken from wiktionary
# versus
# words found in an e-book

# Load the word list
# created by the 01_create-wordlist-from-wiktionary.py

wordlist = set()
with open('words_uniq') as wordlist_file:
    for word in wordlist_file.readlines():
        wordlist.add(word.strip().lower())

print(len(wordlist))

book_path = Path('ebooks/first.txt')

book_wordlist = set()
with open(book_path) as book_file:
    for line in book_file.readlines():
        for word in wordpunct_tokenize(line):
            if word.strip().capitalize()[0] != word.strip()[0] and not any(not c.isalnum() for c in word.strip()):
                book_wordlist.add(word.strip().lower())

unknown_words = book_wordlist - wordlist

print(sorted(list(unknown_words), key=len, reverse=True))
unknown_percentage = 100 * len(unknown_words) / len(book_wordlist)
print(f"Unknown percentage: {round(unknown_percentage, 2)}%")
print(f"Unknown words: {len(unknown_words)}")

