from __future__ import print_function

from lxml import etree
import re
import bz2
import time

from . import WikiPage

class WikiDumpAnalyzer:

    def __init__(self, **kwargs):
        self.language = 'cs'
        self.dump_filename = 'dumps/cswiktionary-20230401-pages-meta-current.xml.bz2'

    def analyze(self):
        total_pages = self.count_pages()
        start = time.perf_counter()
        for i, page in enumerate(self.extract_pages()):
            print(page)

    @staticmethod
    def _get_namespace(tag):
        namespace = re.match("^{(.*?)}", tag).group(1)
        if not namespace.startswith("http://www.mediawiki.org/xml/export-"):
            raise ValueError("%s not recognized as MediaWiki database dump"
                             % namespace)
        return namespace

    def count_pages(self):
        filename = self.dump_filename
        pages_xml = bz2.open(filename, "r")
        cnt = 0
        for event, element in etree.iterparse(pages_xml,
                                              events=["end"]
                                              ):
            if element.tag.endswith("page"):
                cnt += 1
            self.clear_lxml_element(element)
        return cnt

    def extract_pages(self):
        """Extract pages from Wikimedia database dump.
        Returns
        -------
        pages : iterable over WikiPage objects
        """
        filename = self.dump_filename
        pages_xml = bz2.open(filename, "r")

        first = False
        root = None
        namespace = None
        inside_something = False
        inside_revision = False
        for event, element in etree.iterparse(pages_xml, events=["start", "end"]):
            if not first and event == 'start':
                root = element
                namespace = self._get_namespace(element.tag)
                first = True
            # State machine
            if element.tag.endswith("page"):
                if event == 'start':
                    text = None
                    title = None
                    page_id = None
                elif event == 'end':
                    if text is None or title is None or page_id is None:
                        text = None
                        title = None
                        page_id = None
                        self.clear_lxml_element(element)
                        continue
                    yield WikiPage(language=self.language, page_id=page_id, article_title=title, wikitext=text)
                    text = None
                    title = None
                    page_id = None
                    self.clear_lxml_element(element)

            if element.tag.endswith("text") and element.text is not None and not inside_something:
                text = element.text
            if element.tag.endswith(f"{{{namespace}}}id") and element.text is not None \
                    and not inside_something and not inside_revision:
                page_id = int(element.text)
            if element.tag.endswith("title") and element.text is not None and not inside_something:
                title = element.text
            if element.tag.endswith("contributor"):
                if event == 'start':
                    inside_something = True
                else:
                    inside_something = False
            if element.tag.endswith("revision"):
                if event == 'start':
                    inside_revision = True
                else:
                    inside_revision = False
            if event == 'end':
                self.clear_lxml_element(element)

    @staticmethod
    def clear_lxml_element(element: etree.Element):
        # first empty children from current element
        # This is not absolutely necessary if you are also deleting siblings,
        # but it will allow you to free memory earlier.
        element.clear()
        # second, delete previous siblings (records)
        while element.getprevious() is not None:
            del element.getparent()[0]

