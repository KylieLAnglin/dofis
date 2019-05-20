from unittest import TestCase
from data_from_tea.library import clean_tea



class TestClean_ddays(TestCase):
    def test_clean_ddays(self):
        d_ground_truth = {'yr1617': 1203, 'yr1718': 1200}
        for year in ['yr1617', 'yr1718']:
            ddays = clean_tea.clean_ddays(year)
            if year == 'yr1617':
                """
                109 schools in days_yr1617 that are not in dref. 
                All of them appear to be alternative schools, hospitals, DAEP, accelerated schools, JAEP.
                7 schools in desc_c_yr1617 that are not in days.

                274 schools in days_yr1718 that are not in dref. 
                All of them appear to be alternative schools, hospitals, DAEP, accelerated schools, JAEP.
                126 schools in desc_c_yr1718 that are not in days. Not all are charters
                """
                # TODO: cdays_yr1718 is missing a number of campuses
                d_acceptable = ddays.district.nunique() + 2  # missing two charters
            if year == 'yr1718':
                d_acceptable = ddays.district.nunique()
            self.assertEqual(d_ground_truth[year], d_acceptable)
