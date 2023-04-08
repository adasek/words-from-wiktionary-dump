### Words from Wiktionary Dump
Experimental parser to load words from czech wiktionary

#### Running
Obtain latest `cs` dump from https://meta.wikimedia.org/wiki/Data_dumps

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
