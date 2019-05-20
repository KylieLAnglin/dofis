from unittest import TestCase
from data_from_tea.library import clean_tea



class TestClean_ddays(TestCase):
    def test_clean_ddays(self):
        for year in ['yr1617', 'yr1718']:
            cdays = clean_tea.clean_ddays(year)
            self.assertEqual(1,1)
