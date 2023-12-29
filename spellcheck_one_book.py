import pickle
from nltk.tokenize import word_tokenize, sent_tokenize

word_counter_file_name = 'corpus/word_counter.pickle'
book_path = '/home/adam/ebooks/19584254/Knizky elektronicke/Knihy v TXT podle autoru/H/Heinlein, RA/Heinlein Robert A - Dost casu na lasku.txt'
#

def normalize_word(w):
    for char in [*" \u200c –'…"]:
        w = w.strip(char)
    return w.lower()

with open(word_counter_file_name, "rb") as word_counter_file:
    word_counter = pickle.load(word_counter_file)

with open(book_path, 'r', encoding='utf-8') as book_file:

    text = book_file.read()

    sentences = sent_tokenize(text, language='czech')
    cnt = 0
    for sentence in sentences:
        for word in word_tokenize(sentence, language='czech'):
            normalized_word = normalize_word(word)
            if word_counter[normalized_word] <= 1 and word_counter[word] <= 1 and word[0] == word[0].lower():
                cnt += 1
                print(word) # normalized_word
    print(cnt)
