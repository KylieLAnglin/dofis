from unittest import TestCase
from data_from_plans import extract_dates



class TestGet_years(TestCase):
    def test_get_yearss(self):
        text = 'and the community. On February 28, 2017, the Board appointed an eighteen members. March'
        list = extract_dates.get_years(text)
        print(list)
        self.assertIn('2017', list)
        self.assertEqual(1, len(list))

        text = 'and the community. In February, the Board appointed an eighteen members.'
        list = extract_dates.get_years(text)
        print(list)
        self.assertEqual(0, len(list))

        text = ''
        list = extract_dates.get_years(text)
        print(list)
        self.assertEqual(0, len(list))



