from unittest import TestCase
from exemptions import extract_dates



class TestGet_months(TestCase):
    def test_get_months(self):
        text = 'and the community. On February 28, 2017, the Board appointed an eighteen members. March'
        list = extract_dates.get_months(text)
        print(list)
        self.assertIn('February', list)
        self.assertIn('March', list)

        text = 'and the community.'
        list = extract_dates.get_months(text)
        print(list)
        self.assertEqual(0, len(list))