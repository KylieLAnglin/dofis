import unittest
import pandas as pd
from start import data_path
import os

teachers = pd.read_csv(os.path.join(data_path, 'data_from_tea', 'teachers', 'teachers_yr1617.csv'))
teachers['fte_teacher'] = teachers['fte_teacher'].apply(pd.to_numeric, errors='coerce')

class TestNumberTeachers(unittest.TestCase):
    def test_number_teachers(self):
        ground_truth_count = 352756
        test = teachers.fte_teacher.sum()
        print(test) #344973
        test2 = teachers.fte.sum()
        print(test2) #356036
        test3 = teachers[teachers.fte_teacher.notnull()].fte.sum()
        print(test3) #355788
        self.assertTrue(test3 - 3500 <= ground_truth_count <= test3 + 3500)

    def test_number_teachers_district(self):
        leander = teachers[teachers.district == 246913]
        ground_truth_count = 2528
        test = leander.fte_teacher.sum()
        print(test) #2500
        test2 = leander[leander.fte_teacher.notnull()].fte.sum()
        print(test2) #2580
        test3 = leander.fte.sum()
        print(test3)
        self.assertTrue(test - 26 <= ground_truth_count <= test + 26)


if __name__ == '__main__':
    unittest.main()
