from unittest import TestCase
from clean import clean_tea


class TestClean_dref(TestCase):
    def test_clean_dref(self):
        subject_list = ['3rd', '4th', '5th', '6th', '7th', '8th',
                        'Algebra', 'Biology', 'EnglishI', 'EnglishII', 'USHistory']
        year_list = ['yr1112', 'yr1213', 'yr1314', 'yr1415', 'yr1516', 'yr1617', 'yr1718']
        for year in year_list:
            for subject in subject_list:
                clean_tea.clean_scores(year, subject)
        self.assertEqual(1,1)
