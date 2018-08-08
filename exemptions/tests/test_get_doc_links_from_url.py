from unittest import TestCase
from exemptions import gather



class TestGet_doc_links_from_url(TestCase):
    def test_get_doc_links_from_url(self):
        input_url = 'https://www.southsanisd.net/Page/5705'
        identifier = '.pdf'
        title = 'South San Antonio ISD'
        endings_regex = r'"([a-zA-Z\ \/0-9_%\.:?]*\.pdf)"'
        target_url = 'https://www.southsanisd.net//cms/lib/TX01918317/Centricity/Domain/1839/Local%20Innovation%20Plan_%20Approved%204_19_17.pdf'
        test = gather.get_doc_links_from_url(url = input_url, identifier = identifier, title = title, endings_regex = endings_regex)
        self.assertIn(target_url, list(test.keys()))

        input_url = 'https://wildoradoisd.socs.net/vnews/display.v/ART/597b37c5393e1'
        target_url = "https://wildoradoisd.socs.net/vimages/shared/vnews/stories/597b37c5393e1/District%20Innovation%20Plan.docx"
        identifier = '.docx'
        title = 'Wildarado ISD'
        endings_regex = r'([a-zA-Z\ \/0-9_%\.:]*\.docx)'
        test2 = gather.get_doc_links_from_url(url = input_url, identifier = identifier, title = title, endings_regex = endings_regex)
        self.assertIn(target_url, list(test2.keys()))



# def get_doc_links_from_url(url, identifier, title, endings_regex = r'"(.pdf)"'):
# # like here '
# https://www.southsanisd.net//cms/lib/TX01918317/Centricity/Domain/1839/Local Innovation Plan_ Approved 4_19_17.pdf'