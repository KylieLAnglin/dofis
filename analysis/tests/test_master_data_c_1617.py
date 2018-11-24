import unittest
import pandas as pd
import os
from start import data_path


# statistics taken from: https://rptsvr1.tea.texas.gov/perfreport/tapr/2017/state.pdf
class TestCampusDataIntegrity1617(unittest.TestCase):
    def test_number_schools_and_districts(self):
        """
        Statistics taken from # https://tea.texas.gov/WorkArea/DownloadAsset.aspx?id=51539619750
        :return:
        """
        data = pd.read_csv(os.path.join(data_path, 'clean', 'master_data_c.csv'), sep=",")
        data = data[data.year == 'yr1617']
        numschools = data.campus.nunique()
        numdistricts = data.district.nunique()
        self.assertEqual(numschools, 8757)
        self.assertEqual(numdistricts, 1203)


if __name__ == '__main__':
    unittest.main()
