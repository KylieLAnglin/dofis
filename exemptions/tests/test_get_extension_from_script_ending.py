from unittest import TestCase
import gather

class TestGet_extension_from_script_ending(TestCase):
    def test_get_extension_from_script_ending(self):
        input_url = 'http://www.mineolaisd.net/page/District-of-Innovation'
        endings = '.pdf'
        identifier = ',pdf'
        title = 'Mineola ISD'
        test = gather.get_extension_from_script_ending(url =input_url, endings = endings, identifier = identifier, title = title)
        print(test)
        self.fail()

