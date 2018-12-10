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
            self.assertEqual(numstudents, ground_truth_students[yr])

    def test_number_districts_schools_students(self):
        """
        Statistics taken from
        https://tea.texas.gov/Student_Testing_and_Accountability/Testing/State_of_Texas_Assessments_of_Academic_Readiness_(STAAR)/STAAR_Statewide_Summary_Reports_2016-2017/
        :return:
        """
        #TODO solve number of test takers puzzle.
        ground_truth_scores_1617 = {'r_8th_avescore': 1551, 'm_8th_avescore': 1655,
                                    'eng1_avescore': 3922}

        ground_truth_testers_1617 = {'r_8th_numtakers': 380566, 'm_8th_numtakers': 324154,
                                     'eng1_numtakers': 479150} # note english actually fails dues to dropping specialty schools

        data = pd.read_csv(os.path.join(data_path, 'clean', 'master_data_c.csv'), sep=",")

        for yr in ['yr1617']:
            data = data[data.year == yr]
            for sub in ground_truth_testers_1617:
                numtakers = data[sub].sum()
                print(sub, ' ', numtakers)
                self.assertTrue(numtakers - 100 <= ground_truth_testers_1617[sub] <= numtakers + 100)

            """
            for key in ground_truth_testers_1617:
                avescore = data[key].mean()
                print(avescore)
                self.assertEqual(avescore, ground_truth_testers_1617[key])
            """

if __name__ == '__main__':
    unittest.main()
