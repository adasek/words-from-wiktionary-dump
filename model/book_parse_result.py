from pathlib import Path
from collections import Counter
from charset_normalizer import from_bytes
from nltk.tokenize import word_tokenize, sent_tokenize
from helper import normalize_word

import nltk
class BookParseResult:

    def __init__(self, file_name: Path, count_sentences=False):
        self.word_counter = Counter()
        self.word_counter_normalized = Counter()
        self.sentence_counter = Counter()
        self.valid = True
        self.file_name = file_name

        text = self.read_book()
        # Avoid Slovak & nondiacritics texts.
        # Unfortunately the charset_normalizer sometimes falsely identifes the text as Slovak
        # so cannot use matches.best().language to tell.
        if text is None:
            self.valid = False
            return

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
        if count_sentences:
            self.sentence_counter.update(sentences)
        for sentence in sentences:
            for word in word_tokenize(sentence, language='czech'):
                self.word_counter.update([word])
                self.word_counter_normalized.update([normalize_word(word)])

    def read_book(self):
        with open(self.file_name, 'rb') as book_file:
            matches = from_bytes(
                book_file.read(),
                cp_isolation=['cp1250', 'utf-8', 'iso-8859-2'],  # Finite list of encoding to use when searching for a match
            )
        if matches.best() is None:
            self.valid = False
            return
        return matches.best().output('utf-8').decode('utf-8')

    @classmethod
    def parse_book(cls, file_name: Path, count_sentences=False):
        return BookParseResult(file_name, count_sentences=count_sentences)
