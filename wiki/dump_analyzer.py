from __future__ import print_function

from lxml import etree
import re
import bz2
from wikitextparser import remove_markup, parse

from . import WikiPage

class WikiDumpAnalyzer:

    def __init__(self, **kwargs):
        self.language = 'cs'
        self.dump_filename = 'dumps/cswiktionary-20230801-pages-meta-current.xml.bz2'

    def analyze(self):
        template_types = {
            "substantivum (cs)": 1,
            "adjektivum (cs)": 2,
            "číslovka adj (cs)": 2,
            "zájmeno adj (cs)": 2,
            "zájmeno (cs)": 3,
            "číslovka (cs)": 4,
            "sloveso (cs)": 5,
        }
        section_title_types = {
            "čeština>příslovce": 6,
            "čeština>předložka": 7,
            "čeština>spojka": 8,
            "čeština>částice": 9,
            "čeština>citoslovce": 10
        }


        def valid(word):
             return " " not in word and "/" not in word and "-" not in word

        # Build section tree
        def build_section_tree(parsed_wikitext):
            section_to_children = {}
            all_sections = parsed_wikitext.get_sections(include_subsections=True)
            root_section = all_sections[0]
            max_children = 0
            for section in all_sections:
                section_to_children[hash(section.string)] = []
            for section1 in all_sections:
                # print(str(section1.title))
                for section2 in all_sections:
                    if section1 in section2 and section2 in section1:
                        # identical
                        pass
                    elif section1 in section2:
                        section_to_children[hash(section2.string)].append(section1)
                        if len(section_to_children[hash(section2.string)]) > max_children:
                            max_children = len(section_to_children[hash(section2.string)])
                            root_section = section2
            def create_node(section, section_to_children):
                return {
                    'string': section.string,
                    'title': (section.title or "").strip().lower(),
                    'children': [create_node(child, section_to_children) for child in section_to_children[hash(section.string)]]
                }
            return create_node(root_section, section_to_children)


        def get_tree_path(section_tree_node, template):
            if template.string in section_tree_node["string"]:
                for child in section_tree_node["children"]:
                    child_path = get_tree_path(child, template)
                    if len(child_path) > 0:
                        return [section_tree_node] + child_path
                return [section_tree_node]
            else:
                return []


        for i, page in enumerate(self.extract_pages()):
            parsed = parse(page.wikitext)
            section_tree = build_section_tree(parsed)
            # print(section_tree)
            # print("---")

            # print([y.title for x, y in templates_with_deepest_section(parsed) if y.title is not None])
            #print()
            # templates_with_deepest_section(parsed)
            # Section-Template
            # relationship is important to parse the proper Meaning of the word

            # for title, word_type in section_title_types.items():
            #    templates_of_given_type = [template for template in all_templates if is_template(template, template_name)]

            all_templates = [template for template in parsed.templates]

            def is_template(template, template_name):
                    template_name_normalized = template.name.strip().lower()
                    return template_name_normalized == template_name.strip().lower()

            words = []
            for template_name, word_type in template_types.items():
                templates_of_given_type = [template for template in all_templates if is_template(template, template_name)]
                for templ in templates_of_given_type:
                    for arg in templ.arguments:
                        if arg.value.strip().startswith('nesklonné') and arg.name == "1":
                            words += [page.article_title]
                        else:
                            word_form = remove_markup(arg.value.strip())
                            words += [w for w in word_form.split("/") if valid(w)]
                            # print(",".join([node["title"] for node in get_tree_path(section_tree, templ)]))

            for section in parsed.sections:
                tree_path = ">".join([node["title"] for node in get_tree_path(section_tree, section)])
                if tree_path in section_title_types.keys():
                    words += [page.article_title]
            for word in words:
                print(word)



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

