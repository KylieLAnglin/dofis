from unittest import TestCase
from data_from_tea.library import clean_tea_schools

class TestClean_cscores(TestCase):
    def test_clean_cscores(self):
        subject_list = ['3rd', '4th', '5th', '6th', '7th', '8th',
                        'Algebra', 'Biology', 'EnglishI', 'EnglishII', 'USHistory']
        year_list = ['yr1112', 'yr1213', 'yr1314', 'yr1415', 'yr1516', 'yr1617', 'yr1718']
        # year_list = ['yr1213', 'yr1314', 'yr1415', 'yr1516', 'yr1617', 'yr1718']
        for year in year_list:
            for subject in subject_list:
                df = clean_tea_schools.clean_cscores(year, subject)
                print(df.columns)
        self.assertEqual(1, 1)
