from unittest import TestCase
from exemptions import extract_dates


class TestGet_date_phrase_list(TestCase):
    def test_get_date_phrase_list(self):
        test_list = extract_dates.get_date_phrase_list('This plan will begin on September 1, 2016 and will end on September 1, 2021. Includes 21.0033.')
        self.assertEqual(len(test_list), 2)
        self.assertIn('This plan', str(test_list[0][1]))


