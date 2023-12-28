from pathlib import Path
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
from collections import Counter
import pickle
import random
from tqdm import tqdm
import functools
import gc
from more_itertools import chunked
from multiprocessing import Pool, Value
from charset_normalizer import from_bytes

nltk.download('punkt')

def normalize_word(w):
    for char in [*" \u200c –'…"]:
        w = w.strip(char)
    return w.lower()

def is_alfanumeric(word: str) -> bool:
    return not any(not c.isalnum() for c in word.strip())


def save_result(corpus: dict, pickle_filename:Path):
    with open(pickle_filename, 'wb') as outputfile:
        pickle.dump(corpus, outputfile)


# word -> occurrences
word_counter = Counter()
word_counter_normalized = Counter()

# sentence -> occurrences
sentence_counter = Counter()


def parse_book(file_name: Path):
    return BookParseResult(file_name)


class BookParseResult:

    def __init__(self, file_name: Path):
        self.word_counter = Counter()
        self.word_counter_normalized = Counter()
        self.sentence_counter = Counter()
        self.valid = True

        with open(file_name, 'rb') as book_file:
            matches = from_bytes(
                book_file.read(),
                cp_isolation=['cp1250', 'utf-8', 'iso-8859-2'],  # Finite list of encoding to use when searching for a match
            )
        if matches.best() is None:
            self.valid = False
            return
        text = matches.best().output('utf-8').decode('utf-8')
        # Avoid Slovak & nondiacritics texts.
        # Unfortunately the charset_normalizer sometimes falsely identifes the text as Slovak
        # so cannot use matches.best().language to tell.

        if 'č' not in text or 'š' not in text or 'ě' not in text:
            self.valid = False
            return
        if 'ľ' in text:  # or 'ô' in text
            slovak_words_count = 0
            words_count = 0
            for sentence in sent_tokenize(text, language='czech'):
                for word in word_tokenize(sentence, language='czech'):
                    words_count += 1
                    if 'ľ' in word:
                        slovak_words_count += 1
            if slovak_words_count/words_count > 1/20000:
                self.valid = False
                return

        sentences = sent_tokenize(text, language='czech')
        self.sentence_counter.update(sentences)
        for sentence in sentences:
            for word in word_tokenize(sentence, language='czech'):
                self.word_counter.update([word])
                self.word_counter_normalized.update([normalize_word(word)])


book_paths = list(Path('/home/adam/ebooks/19584254/Knizky elektronicke/Knihy v TXT podle autoru/').rglob('*.txt'))


word_counter = Counter()
word_counter_normalized = Counter()
sentence_counter = Counter()

# batches to limit the RAM used
for i, chunk in enumerate(chunked(book_paths, 1000)):
    print(f"Chunk {i}:{len(chunk)}")
    with Pool(processes=8) as pool:
        book_parse_results = list(tqdm(pool.imap_unordered(parse_book, chunk), total=len(chunk)))

    print(f"Adding")
    valid_book_parse_results = [b for b in book_parse_results if b.valid]
    print(f"{len(valid_book_parse_results)} valid out of {len(book_parse_results)}")

    word_counter += functools.reduce(lambda a, b: a+b, map(lambda x: x.word_counter, valid_book_parse_results))
    word_counter_normalized += functools.reduce(lambda a, b: a+b, map(lambda x: x.word_counter_normalized, valid_book_parse_results))
    # sentence_counter += functools.reduce(lambda a, b: a+b, map(lambda x: x.sentence_counter, valid_book_parse_results))

    print(f"Chunk Done")
    valid_book_parse_results = []
    book_parse_results = []
    gc.collect()


save_result(word_counter, f"corpus/word_counter.pickle")
save_result(word_counter_normalized, f"corpus/word_counter_normalized.pickle")

# save_result(sentence_counter, f"corpus/sentence_counter.pickle")

print(sentence_counter.most_common(100))
print(word_counter.most_common(1000))
