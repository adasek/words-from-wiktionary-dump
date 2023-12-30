from pathlib import Path

from collections import Counter
import pickle
import random
from tqdm import tqdm
from datetime import datetime
import functools
import gc
from more_itertools import chunked
from multiprocessing import Pool
from model import BookParseResult
from helper import save_result, counter_reduce

# nltk.download('punkt')

SENTENCE_COUNTER = False

# word -> occurrences
word_counter = Counter()
word_counter_normalized = Counter()

# sentence -> occurrences
sentence_counter = Counter()

book_paths = list(Path('/home/adam/projekty/ebooks-downloader/v2/knihy/').rglob('*.epub')) + \
             list(Path('/home/adam/ebooks/19584254/Knizky elektronicke/').rglob('*.pdb')) + \
             list(Path('/home/adam/ebooks/19584254/Knizky elektronicke/').rglob('*.PDB')) + \
             list(Path('/home/adam/ebooks/19584254/Knizky elektronicke/').rglob('*.txt'))

    # list(Path('/home/adam/ebooks/19584254/Knizky elektronicke/Knihy v TXT podle autoru/').rglob('*.txt'))


word_counter = Counter()
word_counter_normalized = Counter()
sentence_counter = Counter()

# batches to limit the RAM used
for i, chunk in enumerate(chunked(book_paths, 1000)):
    print(f"Chunk {i}:{len(chunk)} {datetime.now()}")
    with Pool(processes=8) as pool:
        book_parse_results = list(tqdm(pool.imap_unordered(BookParseResult.parse_book, chunk), total=len(chunk)))

    print(f"Adding  {datetime.now()}")
    valid_book_parse_results = [b for b in book_parse_results if b is not None and b.valid]
    print(f"{len(valid_book_parse_results)} valid out of {len(book_parse_results)}")
    # for v in valid_book_parse_results:
        # print(v.file_name)
        # print(random.sample(v.read_book().split("\n"), 1))

    word_counter += counter_reduce(list(map(lambda x: x.word_counter, valid_book_parse_results)))
    word_counter_normalized += counter_reduce(list(map(lambda x: x.word_counter_normalized, valid_book_parse_results)))
    if SENTENCE_COUNTER:
        sentence_counter += counter_reduce(list(map(lambda x: x.sentence_counter, valid_book_parse_results)))

    print(f"Chunk Done {datetime.now()}")
    valid_book_parse_results = []
    book_parse_results = []
    gc.collect()
    print(f"Garbage Collected {datetime.now()}")


save_result(word_counter, f"corpus/word_counter3.pickle")
save_result(word_counter_normalized, f"corpus/word_counter_normalized3.pickle")
if SENTENCE_COUNTER:
    save_result(sentence_counter, f"corpus/sentence_counter.pickle")

print(sentence_counter.most_common(100))
print(word_counter.most_common(1000))
