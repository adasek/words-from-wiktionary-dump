from pathlib import Path

from collections import Counter
import pickle
from tqdm import tqdm
from datetime import datetime
import gc
from more_itertools import chunked
from multiprocessing import Pool
from model import BookParseResult
from helper import save_result, counter_reduce, load_counter_pickle

SENTENCE_COUNTER = False

# word -> occurrences
word_counter = Counter()
word_counter_normalized = Counter()

# sentence -> occurrences
sentence_counter = Counter()

book_paths = list(Path('/home/adam/ebooks/19584254/Knizky elektronicke/Knihy v TXT podle autoru/').rglob('*.txt'))

def exotic_words_ratio(word_counter, book_word_counter, threshold=1):
    number_of_exotic_words = 0
    for word, occurrences in book_word_counter.items():
        if word_counter[word] - occurrences <= threshold:
            number_of_exotic_words += 1
    words_in_book = sum(book_word_counter.values())
    if words_in_book == 0:
        return 1
    else:
        return number_of_exotic_words / words_in_book

word_counter = Counter()
word_counter_normalized = Counter()
sentence_counter = Counter()

def parse_book2(file_name: Path):
    result = BookParseResult(file_name, count_sentences=SENTENCE_COUNTER)
    exotic_ratio = exotic_words_ratio(global_word_counter, result.word_counter)
    if result.valid and exotic_ratio > 0.02:
        result.valid = False
        print(exotic_ratio)
        print(file_name)
        # print(result.read_book())
        # TMP:
        for word, occurrences in result.word_counter.items():
            if global_word_counter[word] - occurrences <= 1:
                print(word)
    return result

# batches to limit the RAM used
for i, chunk in enumerate(chunked(book_paths, 1000)):
    print(f"Chunk {i}:{len(chunk)} {datetime.now()}")

    global_word_counter = load_counter_pickle("corpus/word_counter.pickle")
    with Pool(processes=8) as pool:
        book_parse_results = list(tqdm(pool.imap_unordered(parse_book2, chunk), total=len(chunk)))

    print(f"Adding  {datetime.now()}")
    valid_book_parse_results = [b for b in book_parse_results if b.valid]
    print(f"{len(valid_book_parse_results)} valid out of {len(book_parse_results)}")

    word_counter += counter_reduce(list(map(lambda x: x.word_counter, valid_book_parse_results)))
    word_counter_normalized += counter_reduce(list(map(lambda x: x.word_counter_normalized, valid_book_parse_results)))
    if SENTENCE_COUNTER:
        sentence_counter += counter_reduce(list(map(lambda x: x.sentence_counter, valid_book_parse_results)))

    print(f"Chunk Done {datetime.now()}")
    valid_book_parse_results = []
    book_parse_results = []
    gc.collect()
    print(f"Garbage Collected {datetime.now()}")


save_result(word_counter, f"corpus/word_counter2.pickle")
save_result(word_counter_normalized, f"corpus/word_counter_normalized2.pickle")
if SENTENCE_COUNTER:
    save_result(sentence_counter, f"corpus/sentence_counter2.pickle")

print(sentence_counter.most_common(100))
print(word_counter.most_common(1000))
