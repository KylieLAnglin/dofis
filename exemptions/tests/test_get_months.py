from unittest import TestCase
from exemptions import extract_dates


class TestGet_months(TestCase):
    def test_get_months(self):
        text = 'and the community. On February 28, 2017, the Board appointed an eighteen members. March'
        list = extract_dates.get_months(text)
        print(list)
        self.assertIn('February', list)
        self.assertIn('March', list)

        text = 'local business owners. On January 17, 2017, the District Education Improvement Committee.'
        list = extract_dates.get_months(text)
        print(list)
        self.assertIn('January', list)
        self.assertEqual(1, len(list))

        text = 'and the community.'
        list = extract_dates.get_months(text)
        print(list)
        self.assertEqual(0, len(list))

        text = ''
        list = extract_dates.get_months(text)
        print(list)
        self.assertEqual(0, len(list))
