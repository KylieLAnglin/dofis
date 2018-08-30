from unittest import TestCase
from exemptions import extract_dates

class TestGet_latest_month_year_pair(TestCase):
    def test_get_latest_month_year_pair(self):
        test = 'final Local Innovation Plan on March-May 2017* February 28, 2017'
        year, month = extract_dates.get_latest_month_year_pair(test)
        print(month, year)
        self.assertEqual('May', month)
        self.assertEqual(2017, year)

        test2 = 'hello'
        year, month = extract_dates.get_latest_month_year_pair(test2)
        self.assertEqual('', month)
        self.assertEqual(-999, year)

