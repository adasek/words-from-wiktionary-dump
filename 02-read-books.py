from pathlib import Path
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
from collections import Counter
import pickle
import random
from charset_normalizer import from_bytes

nltk.download('punkt')


book_paths = Path('/home/adam/ebooks/19584254/Knizky elektronicke/Knihy v TXT podle autoru/').rglob('*.txt')


def is_alfanumeric(word: str) -> bool:
    return not any(not c.isalnum() for c in word.strip())


def save_result(corpus: dict, pickle_filename:Path):
    with open(pickle_filename, 'wb') as outputfile:
        pickle.dump(corpus, outputfile)


# word -> occurrences
word_counter = Counter()

# sentence -> occurrences
sentence_counter = Counter()

for i, book_path in enumerate(book_paths):
    #try:
        with open(book_path, 'rb') as book_file:
            matches = from_bytes(
                book_file.read(),
                cp_isolation=['cp1250', 'utf-8', 'iso-8859-2'],  # Finite list of encoding to use when searching for a match
            )
            text = matches.best().output('utf-8').decode('utf-8')
            # Avoid Slovak & nondiacritics texts.
            # Unfortunately the charset_normalizer sometimes falsely identifes the text as Slovak
            # so cannot use matches.best().language to tell.

            if 'č' not in text or 'š' not in text or 'ě' not in text:
                print()
                print(text[2000:3000])
                continue

            sentences = sent_tokenize(text, language='czech')
            sentence_counter.update(sentences)
            for sentence in sentences:
                word_counter.update([word for word in word_tokenize(sentence, language='czech')])
        print(".", end="", flush=True)
    #except UnicodeDecodeError:
    #    print("!", end="", flush=True)
    # if i % 1000 == 0:
        # save_result(corpus)
save_result(word_counter, f"corpus/word_counter.pickle")
save_result(sentence_counter, f"corpus/sentence_counter.pickle")

print(sentence_counter.most_common(100))
print(word_counter.most_common(100))
