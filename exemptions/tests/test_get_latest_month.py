from unittest import TestCase
from exemptions import extract_dates


class TestGet_latest_month(TestCase):
    def test_get_latest_month(self):
        test = ['February', 'March']
        self.assertEqual('March', extract_dates.get_latest_month(test))

        test = []
        self.assertEqual('', extract_dates.get_latest_month(test))
