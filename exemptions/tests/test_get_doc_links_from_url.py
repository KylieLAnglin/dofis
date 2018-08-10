from unittest import TestCase
from exemptions import gather_documents


class TestGet_doc_links_from_url(TestCase):
    def test_get_doc_links_from_url(self):

        # Simple case
        input_url = 'https://wildoradoisd.socs.net/vnews/display.v/ART/597b37c5393e1'
        target_url = "https://wildoradoisd.socs.net/vimages/shared/vnews/stories/597b37c5393e1/District%20Innovation%20Plan.docx"
        identifier = '.docx'
        title = 'Wildorado ISD'
        test1 = gather_documents.get_doc_links_from_href_scripts_iframes(url = input_url, identifier = identifier, title = title, strings_of_interest=['.docx'], kind ='ending')
        self.assertIn(target_url, list(test1.keys()))

        # Example iframe? Or script
        input_url = 'http://www.ldisd.net/Page/4495'
        target_url = "http://www.ldisd.net//cms/lib5/TX01817232/Centricity/Domain/2021/InnovationPlan_1-25-2017.pdf"
        identifier = 'google'
        title = 'Lake Dallas ISD'
        test2 = gather_documents.get_doc_links_from_href_scripts_iframes(url = input_url, identifier = identifier, title = title, strings_of_interest=['.pdf'], kind ='ending')
        self.assertIn(target_url, list(test2.keys()))

        # Simple example
        input_url = 'https://www.aliefisd.net/Page/8915'
        target_url = 'https://www.aliefisd.net/site/handlers/filedownload.ashx?moduleinstanceid=14757&dataid=16197&FileName=Approved%20Alief%20District%20of%20Innovation%20Plan.pdf'
        identifier = '.pdf'
        title = "Alief ISD"
        test3 = gather_documents.get_doc_links_from_href_scripts_iframes(url=input_url, identifier=identifier, title=title,
                                                                         strings_of_interest=['.pdf'], kind='contains')
        self.assertIn(target_url, list(test3.keys()))

        # Example Google Doc
        input_url = 'http://www.woisd.net/district-of-innovation/'
        target_url = "https://docs.google.com/document/d/1otlNz4M2ppxfasw8G8Uq2CJnHBRJ65xRr6fdKj4VsJI/edit?usp=sharing"
        identifier = 'google'
        title = 'google'
        test4 = gather_documents.get_doc_links_from_href_scripts_iframes(url = input_url, identifier = identifier, title = title, strings_of_interest=['docs.google'], kind ='contains')
        self.assertIn(target_url, list(test4.keys()))





