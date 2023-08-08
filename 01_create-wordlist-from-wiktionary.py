from wiki import WikiDumpAnalyzer
import json

def contains_special_characters(word: str) -> bool:
    return any(not c.isalnum() for c in word)

wiki_dump_analyzer = WikiDumpAnalyzer('dumps/cswiktionary-20230801-pages-meta-current.xml.bz2')

all_words = list()
words_to_lemmas = {}

for lemma, word in wiki_dump_analyzer.analyze():
    existing_lemma = words_to_lemmas[word.lower()] if word.lower() in words_to_lemmas else None
    all_words.append(word)
    if not contains_special_characters(lemma) and not contains_special_characters(word) and \
            existing_lemma != word:
        words_to_lemmas[word] = lemma

uniq_words = set(all_words)

with open('words', 'w') as words_file:
    for word in all_words:
        print(word, file=words_file)

with open('words_to_lemmas', 'w') as words_to_lemmas_file:
    for lemma, word in words_to_lemmas.items():
        print(f"{word},{lemma}", file=words_to_lemmas_file)

with open('words_uniq', 'w') as words_uniq_file:
    for word in uniq_words:
        print(word, file=words_uniq_file)

with open("words_to_lemmas.json", "w") as words_to_lemmas_json_file:
    words_to_lemmas_json_file.write(json.dumps(words_to_lemmas, indent=4))
