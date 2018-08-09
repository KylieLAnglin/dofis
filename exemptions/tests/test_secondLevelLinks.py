from unittest import TestCase
from exemptions import gather


class TestSecondLevelLinks(TestCase):
    title = 'Wildarado ISD'
    url = 'https://wildoradoisd.socs.net/vnews/display.v/ART/597b37c5393e1'
    target_url = 'https://wildoradoisd.socs.net/vimages/shared/vnews/stories/597b37c5393e1/District%20Innovation%20Plan.docx'
    test_dict = {title: url}
    docs_dict = {}

    def test_crawl(self):
        test = gather.SecondLevelLinks(self.test_dict)
        self.assertIn(self.target_url, list(test.doc_links.keys()))

    def test__get_tricky_docs(self):
        title = 'Wildarado ISD'
        url = 'https://wildoradoisd.socs.net/vnews/display.v/ART/597b37c5393e1'
        test = gather.SecondLevelLinks(self.test_dict)
        test._get_tricky_docs(url=url, title=title)
        self.assertIn(self.target_url, list(test.doc_links.keys()))
