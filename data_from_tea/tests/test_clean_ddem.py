from unittest import TestCase
from data_from_tea.library import clean_tea


class TestClean_dref(TestCase):
    def test_clean_ddem(self):
        year_list = ['yr1112', 'yr1213', 'yr1314', 'yr1415', 'yr1516', 'yr1617', 'yr1718']
        ground_truth_teachers = {'yr1112' : 324213, 'yr1213': 327420, 'yr1314': 334511, 'yr1415': 342192,
                                 'yr1516': 347272, 'yr1617': 352756, 'yr1718': 356909}

        for year in year_list:
            data = clean_tea.clean_ddem(year)
            teachers_num = data.teachers_num.sum()
            self.assertTrue(teachers_num - 100 <= ground_truth_teachers[year] <= teachers_num + 100)
        self.assertEqual(1,1)
