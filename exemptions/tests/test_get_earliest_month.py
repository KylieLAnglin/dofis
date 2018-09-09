from unittest import TestCase
from exemptions import extract_dates

class TestGet_earliest_month(TestCase):
    def test_get_earliest_month(self):

        text = ['January', 'February']
        test = extract_dates.get_earliest_month(text)
        self.assertEqual('January', test)