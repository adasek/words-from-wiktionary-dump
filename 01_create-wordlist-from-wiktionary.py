from wiki import WikiDumpAnalyzer

wiki_dump_analyzer = WikiDumpAnalyzer('dumps/cswiktionary-20230801-pages-meta-current.xml.bz2')

words = set()
with open('words', 'w') as words_file, open('words_to_lemmas', 'w') as words_to_lemmas_file:
    for lemma, word in wiki_dump_analyzer.analyze():
        words.add(word)
        print(word, file=words_file)
        if "," not in lemma and "," not in word:
            print(f"{word},{lemma}", file=words_to_lemmas_file)

with open('words_uniq', 'w') as words_uniq_file:
    print(word, file=words_uniq_file)
