from unittest import TestCase
from clean.library import clean_tea
from clean.library import clean_tea_schools

class TestClean_cref(TestCase):
    def test_clean_cref(self):
        year_list = ['yr1112', 'yr1213', 'yr1314', 'yr1415', 'yr1516', 'yr1617', 'yr1718']
        for year in year_list:
            clean_tea.clean_cref(year)
        for year in year_list:
            print(year)
            clean_tea_schools.clean_cref(year)
        self.assertEqual(1,1)
