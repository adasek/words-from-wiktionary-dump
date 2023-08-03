### Words from Wiktionary Dump
Experimental parser to load words from czech wiktionary


#### Running
Obtain latest `cs` dump from https://meta.wikimedia.org/wiki/Data_dumps / https://dumps.wikimedia.org/backup-index.html
```
záda, plavky, nůžky

listí, stromoví, panstvo, námořnictvo

písek, mouka, pivo, zlato

{{Substantivum (cs)
  | snom = vole
  | sgen = volete
  | sdat = voleti
  | sacc = vole
  | svoc = vole
  | sloc = voleti
  | sins = voletem
  | pnom = volata
  | pgen = [[volat]]
  | pdat = volatům
  | pacc = volata
  | pvoc = volata
  | ploc = volatech
  | pins = volaty
}}

==== skloňování ====
{{Substantivum (cs)
  | pnom = záda
  | pgen = zad
  | pdat = zádům
  | pacc = záda
  | pvoc = záda
  | ploc = zádech
  | pins = zády
}}

==== význam ====
Lorem ipsum
```


```python
parsed.sections[1].title
parsed.sections[1].templates[0].name
'Substantivum (cs)\n  '




def normalize_text(text):
	return text.lower().strip()


parsed.sections[1].templates[0].arguments[0]
parsed.sections[1].templates[0].arguments[0].name
' pnom '

parsed.sections[1].templates[0].arguments[0].value
' záda\n  '

from wikitextparser import remove_markup
remove_markup(parsed.sections[0].templates[0].arguments[8].value).strip()
```

```bash
poetry run python3 run.py > out3.txt
sort out3.txt | uniq | sort -R > out3_uniq_random.txt
```


  * https://cs.wiktionary.org/wiki/Kategorie:%C4%8Cesk%C3%A9_%C4%8D%C3%A1stice
    * https://cs.wiktionary.org/wiki/na%C5%A1t%C4%9Bst%C3%AD
  * https://cs.wiktionary.org/w/index.php?title=%C5%A0ablona:Sloveso%20(cs)&redirect=no
```
{{Sloveso (cs)
  | spre1 = mažu
  | ppre1 = mažeme
  | spre2 = mažeš
  | ppre2 = mažete
  | spre3 = maže
  | ppre3 = mažou
  | pimp1 = mažme
  | simp2 = maž
  | pimp2 = mažte
  | sactm = mazal
  | pactm = mazali
  | sactf = mazala
  | pactf = mazaly
  | sactn = mazalo
  | spasm = mazán
  | ppasm = mazáni
  | spasf = mazána
  | ppasf = mazány
  | spasn = mazáno
  | ptram = maže
  ##### Přechodníky
  | ptraf = mažíc
  | ptrap = mažíce
  | mtra = skrýt
}}

# ignoruj fut klíč, a
  pre = skrýt
# | imp = skrýt
# | act = skrýt
# | pas = skrýt
# | ptra = skrýt
# | mtra = skrýt

Nesklonná substantiva
{{Substantivum (cs)
  | nesklonné
}}

Nesklonná pouze plurál

{{Substantivum (cs)
  | nesklonné plurál
}}
```

#### Experiment 2023-08
```bash
poetry run python3 run.py > ./words && sort ./words|uniq > ./words_uniq 

```


#### Todo
 * wikitextparser -> tree
 * podstatné jméno > význam
 * podstatné jméno > skloňování
