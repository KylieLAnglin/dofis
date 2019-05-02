from unittest import TestCase
from data_from_tea.library import clean_tea_schools

class TestClean_cdem(TestCase):
    def test_clean_cdem(self):
        # Number of students fom https://tea.texas.gov/communications/pocket-edition/
        year_list = ['yr1112', 'yr1213', 'yr1314', 'yr1415', 'yr1516', 'yr1617', 'yr1718']
        ground_truth_students = {'yr1112': 4978120, 'yr1213': 5058939, 'yr1314': 5135880, 'yr1415': 5215282,
                        'yr1516': 5284252, 'yr1617': 5343834, 'yr1718': 5385012}
        ground_truth_teachers = {'yr1112' : 324213, 'yr1213': 327420, 'yr1314': 334511, 'yr1415': 342192,
                                 'yr1516': 347272, 'yr1617': 352756, 'yr1718': 356909}
        # Note: in yr1718 pocket edition lists number of students as 5399682. Btu statewide data lists 5385012
        # statewide data from from: https://rptsvr1.tea.texas.gov/perfreport/tapr/2018/download/DownloadData.html
        for year in year_list:
            data = clean_tea_schools.clean_cdem(year)
            students_num = sum(data.students_num)
            teachers_num = data.teachers_num.sum()
            print(str(year) + ':' + str(teachers_num))
            self.assertEqual(students_num,ground_truth_students[year])
            self.assertTrue(teachers_num - 3000 <= ground_truth_teachers[year] <= teachers_num + 3000)

