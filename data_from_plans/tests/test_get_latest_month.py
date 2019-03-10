from unittest import TestCase
from data_from_plans import extract_dates


class TestGet_latest_month(TestCase):
    def test_get_latest_month(self):
        test = ['February', 'March']
        self.assertEqual('March', extract_dates.get_latest_month(test))

        test = []
        result = extract_dates.get_latest_month(test)
        print(result)
        self.assertEqual('', result)

        test = ['January']
        result = extract_dates.get_latest_month(test)
        print(result)
        self.assertEqual('January', result)
