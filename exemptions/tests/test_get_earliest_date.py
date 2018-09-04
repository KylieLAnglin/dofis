from unittest import TestCase
from exemptions import extract_dates

class TestGet_earliest_date(TestCase):
    def test_get_earliest_date(self):
        text = 'This plan will begin on September 1, 2016 and will end on September 1, 2021, 00000.'
        test = extract_dates.get_earliest_date(text)
        self.assertEqual(test, 2016)

        text = 'local business owners. On January 17, 2017, the District Education Improvement Committee.'
        test = extract_dates.get_earliest_date(text)
        self.assertEqual(test, 2017)

        text = ''
        test = extract_dates.get_earliest_date(text)
        self.assertEqual(test, -999)
