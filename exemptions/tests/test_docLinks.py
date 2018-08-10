from unittest import TestCase
from exemptions import gather_documents


class TestDocLinks(TestCase):

    def test__get_docs(self):
        url = 'https://tea.texas.gov/Texas_Schools/District_Initiatives/Districts_of_Innovation/'
        docs_df = gather_documents.FirstLevelLinks(url, print_interim = False).docs_df

        # PDF
        test_pdf_df = docs_df[docs_df.type == "pdf"]
        self.assertIn('http://www.lfcisd.net/UserFiles/Servers/Server_758/File/LF/District%20of%20Innovation%20Plan%20pages.pdf',
                      list(test_pdf_df[test_pdf_df.index == 'Los Fresnos CISD'].link))

        # Word
        test_word_df = docs_df[docs_df.type == "docx"]
        self.assertIn('http://www.marionisd.net/upload/page/0020/DofI%20Plan.docx',
            list(test_word_df[test_word_df.index == 'Marion ISD'].link))

        # Google
        test_google_df = docs_df[docs_df.type == "google"]
        self.assertIn('https://drive.google.com/file/d/0ByTbbvh_1OW_c2pWakJiNENNZXM/preview',
            list(test_google_df[test_google_df.index == 'Morton ISD'].link))

