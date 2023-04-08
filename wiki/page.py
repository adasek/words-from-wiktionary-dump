import rdflib
import urllib
import re

class WikiPage:
    """
        Wiki Page
    """

    def __init__(self, page_id=None, article_title=None, wikitext=None, language=None, revision=None):
        self.page_id = page_id
        self.article_title = article_title
        self.wikitext = wikitext
        self.language = language
        self.revision = revision


    def __str__(self):
        return str(self.article_title) + ":\n" + str(self.wikitext)
    def title_url(self):
        return urllib.parse.quote(self.article_title)

    @staticmethod
    def split_parentheses(text: str):
        if re.match(r'^[^(]* \(.*\)$', text):
            return (True, text.split('(')[0], text.split('(')[1][:-1])
        else:
            return (False, text, '')
            # todo: insert a word meaning based on the () value
