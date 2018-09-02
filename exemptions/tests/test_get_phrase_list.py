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

        test_list = extract_dates.get_phrase_list('')
        self.assertEqual(len(test_list), 0)

        test_list = extract_dates.get_phrase_list('2017')
        self.assertEqual(len(test_list), 1)
        self.assertEqual(test_list[0], '2017')

        test = 'ECISD District of Innovation Plan 1 I. Introduction House Bill 1842, passed during the 84th ' \
               'Legislative Session, permits Texas public school districts to become Districts of Innovation and to ' \
               'obtain exemption from certain provisions of the Texas Education Code. The plan will begin in March of 2017.'
        test_list = extract_dates.get_phrase_list(test)
        print(test_list)



