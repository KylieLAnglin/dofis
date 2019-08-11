from unittest import TestCase
from data_from_tea.library import clean_tea



class TestClean_ddays(TestCase):
    def test_clean_ddays(self):
        d_ground_truth = {'yr1617': 1203, 'yr1718': 1200}
        for year in ['yr1617', 'yr1718']:
            ddays = clean_tea.clean_ddays(year)
            if year == 'yr1617':
                d_acceptable = ddays.district.nunique() + 2  # missing two charters
            if year == 'yr1718':
                d_acceptable = ddays.district.nunique()
                print(d_acceptable)
            self.assertEqual(d_ground_truth[year], d_acceptable)
