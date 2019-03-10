from unittest import TestCase
from data_from_plans import extract_dates

class TestGet_earliest_month_year_pair(TestCase):
    def test_get_earliest_month_year_pair(self):
        text = 'local business owners. On January 17, 2017, the District Education Improvement Committee.'
        year, month = extract_dates.get_earliest_month_year_pair(text)
        self.assertEqual(2017, year)
        self.assertEqual('January', month)
