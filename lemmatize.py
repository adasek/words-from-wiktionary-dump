import csv
from nltk.tokenize import word_tokenize

lemmas = {}
with open('words_to_lemmas') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        #  and (row[0] not in lemmas or len(row[1]) < len(lemmas[row[0]]))
        # row[1].lower() == row[0]
        if ":" not in row[1] and (row[0] not in lemmas or lemmas[row[0]] != row[0]):
            lemmas[row[0]] = row[1]

sentences = """
Rozdělovat dřevo na menší kousky pomocí sekyry, nebo klínku.
Krátce, prudce a zpravidla bolestivě sevřít malý kousek pokožky mezi dva prsty či nehty.
Bodat (od hmyzu)
Označovat a znehodnotit jízdenku
Dráždit
"""

def contains_special_characters(word: str) -> bool:
    return any(not c.isalnum() for c in word)

for sentence in sentences.split("\n"):
    words = word_tokenize(sentence)
    for word in words:
        if (contains_special_characters(word)):
            print(word, end=" ")
        elif word.lower() in lemmas:
            lemma = lemmas[word.lower()]
            if lemma == word:
                print(f"[[{word}]]", end=" ")
            elif word.startswith(lemma):
                rest = word[len(lemma):]
                print(f"[[{lemma}]]{rest}", end=" ")
            else:
                print(f"[[{lemma}|{word}]]", end=" ")
        else:
            print(f"[[???|{word}]]", end=" ")
    print()
