from unittest import TestCase
from data_from_tea.library import clean_tea
from data_from_tea.library import clean_tea_schools

class TestClean_cref(TestCase):
    def test_clean_cref(self):
        # Number of campuses come from TEA Pocket Edition: https://tea.texas.gov/communications/pocket-edition/
        ground_truth = {'yr1112': 8529, 'yr1213': 8555, 'yr1314': 8574, 'yr1415': 8646, 'yr1516': 8673, 'yr1617': 8757, 'yr1718': 8759}
        year_list = ['yr1112', 'yr1213', 'yr1314', 'yr1415', 'yr1516', 'yr1617', 'yr1718']
        for year in year_list:
            data = clean_tea.clean_cref_numschools(year)
            numschools = sum(data.schools_num)
            self.assertEqual(numschools, ground_truth[year])

        for year in year_list:
            data = clean_tea_schools.clean_cref(year)
            self.assertEqual(data.campus.nunique(), ground_truth[year])
