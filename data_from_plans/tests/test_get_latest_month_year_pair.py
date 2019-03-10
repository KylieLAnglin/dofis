from unittest import TestCase
from data_from_plans import extract_dates

class TestGet_latest_month_year_pair(TestCase):
    def test_get_latest_month_year_pair(self):
        test = 'final Local Innovation Plan on March-May 2017* February 28, 2017'
        year, month = extract_dates.get_latest_month_year_pair(test)
        self.assertEqual('May', month)
        self.assertEqual(2017, year)

        test2 = 'hello'
        year, month = extract_dates.get_latest_month_year_pair(test2)
        self.assertEqual('', month)
        self.assertEqual(-999, year)

        test3 = 'meetings held March 23 and April 13, 2016. The Committee obtained input'
        year, month = extract_dates.get_latest_month_year_pair(test3)
        self.assertEqual('April', month)
        self.assertEqual(2016, year)

        test3 = 'local business owners. On January 17, 2017, the District Education Improvement Committee.'
        year, month = extract_dates.get_latest_month_year_pair(test3)
        print(month, year)
        self.assertEqual('January', month)
        self.assertEqual(2017, year)

        test3 = ''
        year, month = extract_dates.get_latest_month_year_pair(test3)
        self.assertEqual('', month)
        self.assertEqual(-999, year)

        test = 'plan for minimum 30 days January 19, 2017 Public DOI meeting January 19'
        year, month = extract_dates.get_latest_month_year_pair(test)
        self.assertEqual('January', month)
        self.assertEqual(2017, year)