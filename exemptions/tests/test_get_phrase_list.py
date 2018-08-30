from unittest import TestCase
from exemptions import extract_dates


class TestGet_phrase_list(TestCase):
    def test_get_phrase_list(self):
        test_list = extract_dates.get_phrase_list('This plan will begin on September 1, 2016 and will end on September 1, 2021. Includes 21.0033 and 00000.')
        self.assertEqual(len(test_list), 2)
        self.assertIn('This plan', str(test_list[0]))

        test_list = extract_dates.get_phrase_list('Sulphur Bluff ISD District Of Innovation Plan 2017-2018 School Year To 2021-2022 School Year')
        self.assertEqual(len(test_list), 4)
        self.assertIn('Sulphur', str(test_list[0]))

        test_list = extract_dates.get_phrase_list('Sulphur Bluff ISD District Of Innovation Plan')
        self.assertEqual(len(test_list), 0)

