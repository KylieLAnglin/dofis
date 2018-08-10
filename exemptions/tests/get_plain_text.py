from unittest import TestCase
from exemptions import clean_documents



class TestGet_link_contents(TestCase):
    def test_get_plain_text(self):
        # simple case
        url = 'http://www.hsisd.net/upload/page/0061/docs/HSISDs%20DOI%20Plan%20-Board%20Approval%20Copy.pdf'
        test_text = 'Empowerment to innovate and think differently.'
        text = clean_documents.get_plain_text(url)
        self.assertIn(test_text, text)

        # error
        url = 'htt#p://www.hsisd.net/upload/page/0061/docs/HSISDs%20DOI%20Plan%20-Board%20Approval%20Copy.pdf'
        test_text = 'UNAVAILABLE'
        text = clean_documents.get_plain_text(url)
        self.assertEqual(test_text, text)

        # google doc
        url = 'https://docs.google.com/document/d/1dg3O2cF88tqTy1OCTPbUv9S2_oPegKY2dnDVXpczoEU/pub'
        test_text = 'To access these flexibilities, a school district must adopt an innovation plan'
        text = clean_documents.get_plain_text(url)
        self.assertIn(test_text, text)

        # word doc
        url = 'https://s3.amazonaws.com/scschoolfiles/1286/campus_improvement_plan_2017-2018_2.docx'
        test_text = 'By 2018-2019, 100% of Wheeler ISD students'
        text = clean_documents.get_plain_text(url)
        self.assertIn(test_text, text)

        # html
        url = 'http://www.chisd.net/Page/9668'
        test_text = '\n'
        text = clean_documents.get_plain_text(url)
        self.assertIn(test_text, text)

