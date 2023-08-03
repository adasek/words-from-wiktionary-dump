from wiki import WikiDumpAnalyzer

wiki_dump_analyzer = WikiDumpAnalyzer('dumps/cswiktionary-20230801-pages-meta-current.xml.bz2')

wiki_dump_analyzer.analyze()
