from unittest import TestCase
from exemptions import gather

#(url, identifier, title, strings_of_interest, kind)

class TestGet_doc_links_from_url(TestCase):
    def test_get_doc_links_from_url(self):

        input_url = 'https://wildoradoisd.socs.net/vnews/display.v/ART/597b37c5393e1'
        target_url = "https://wildoradoisd.socs.net/vimages/shared/vnews/stories/597b37c5393e1/District%20Innovation%20Plan.docx"
        identifier = '.docx'
        title = 'Wildorado ISD'
        test1 = gather.get_doc_links_from_url(url = input_url, identifier = identifier, title = title, strings_of_interest=['.docx'], kind = 'ending')
        self.assertIn(target_url, list(test1.keys()))

        #input_url = 'http://www.trisd.org/district-reports-bd48d186'
        #target_url = 'https://drive.google.com/file/d/0BzSPw2RwwPZaOGVZYmprSGh0V2s/view'
        #identifier = 'google'
        #title = "Three Rivers ISD"
        #test2 = gather.get_doc_links_from_url(url=input_url, identifier=identifier, title=title,
         #                                     strings_of_interest=['drive.google'], kind='contains')
        #self.assertIn(target_url, list(test2.keys()))

        input_url = 'https://www.aliefisd.net/Page/8915'
        target_url = 'https://www.aliefisd.net/site/handlers/filedownload.ashx?moduleinstanceid=14757&dataid=16197&FileName=Approved%20Alief%20District%20of%20Innovation%20Plan.pdf'
        identifier = '.pdf'
        title = "Alief ISD"
        test3 = gather.get_doc_links_from_url(url=input_url, identifier=identifier, title=title,
                                              strings_of_interest=['.pdf'], kind='contains')
        self.assertIn(target_url, list(test3.keys()))





