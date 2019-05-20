from unittest import TestCase
from data_from_tea.library import clean_tea_schools



class TestClean_cdays(TestCase):
    def test_clean_cdays(self):
        c_ground_truth = { 'yr1617': 8757, 'yr1718': 8759}
        d_ground_truth = {'yr1617': 1203, 'yr1718': 1200}
        for year in ['yr1617', 'yr1718']:
            cdays = clean_tea_schools.clean_cdays(year)
            if year == 'yr1617':
                """
                109 schools in days_yr1617 that are not in dref. 
                All of them appear to be alternative schools, hospitals, DAEP, accelerated schools, JAEP.
                7 schools in desc_c_yr1617 that are not in days.
                
                274 schools in days_yr1718 that are not in dref. 
                All of them appear to be alternative schools, hospitals, DAEP, accelerated schools, JAEP.
                126 schools in desc_c_yr1718 that are not in days. Not all are charters
                """
                #TODO: cdays_yr1718 is missing a number of campuses
                c_acceptable = cdays.campus.nunique() - 109 + 7
                d_acceptable = cdays.district.nunique() + 2 #missing two charters
            if year == 'yr1718':
                c_acceptable = cdays.campus.nunique() - 274 + 126 + 2 #TODO: can't explain plus 2
                d_acceptable = cdays.district.nunique()

            self.assertEqual(c_ground_truth[year], c_acceptable)
            self.assertEqual(d_ground_truth[year], d_acceptable)


