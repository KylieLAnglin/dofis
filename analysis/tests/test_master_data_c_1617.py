import unittest
import pandas as pd
import os
from start import data_path


# statistics taken from: https://rptsvr1.tea.texas.gov/perfreport/tapr/2017/state.pdf
class TestCampusDataIntegrity1617(unittest.TestCase):
    def test_number_districts_schools_students(self):
        """
        Statistics taken from # https://tea.texas.gov/WorkArea/DownloadAsset.aspx?id=51539619750
        :return:
        """
        ground_truth_districts = {'yr1617': 1203}
        ground_truth_schools = {'yr1617': 8757}
        ground_truth_students = {'yr1617': 5343834}

        data = pd.read_csv(os.path.join(data_path, 'clean', 'master_data_c.csv'), sep=",")

        for yr in ['yr1617']:
            data = data[data.year == yr]
            numdistricts = data.district.nunique()
            numschools = data.campus.nunique()
            numstudents = data.students_num.sum()
            self.assertEqual(numdistricts, ground_truth_districts[yr])
            self.assertEqual(numschools, ground_truth_schools[yr])
            self.assertEqual(numstudents, ground_truth_students[yr]) #TODO: schools wrong



if __name__ == '__main__':
    unittest.main()
