from unittest import TestCase
from data_from_plans import extract_dates
from data_from_plans import start
import os

class TestNarrow_phrase_list(TestCase):
    def test_narrow_phrase_list(self):
        phrases = ['The plan was drafted on June 1, 2016', 'The plan will begin on August 2, 2017', 'hello']
        output_dir = os.path.join(start.data_path, 'date_finalize_classifier')
        narrowed_phrases, p_list = extract_dates.narrow_phrase_list(phrases, output_dir)
        self.assertEqual(2, len(narrowed_phrases))
        max_phrase, p_list = extract_dates.narrow_phrase_list(phrases, output_dir, just_max= True)
        self.assertEqual(1, len(max_phrase))

        phrases = []
        output_dir = os.path.join(start.data_path, 'date_finalize_classifier')
        narrowed_phrases, p_list = extract_dates.narrow_phrase_list(phrases, output_dir)
        self.assertEqual(0, len(narrowed_phrases))
        max_phrase, p_list = extract_dates.narrow_phrase_list(phrases, output_dir, just_max = True)
        self.assertEqual(0, len(max_phrase))

        phrases = ['2017']
        output_dir = os.path.join(start.data_path, 'date_finalize_classifier')
        narrowed_phrases, p_list = extract_dates.narrow_phrase_list(phrases, output_dir)
        print(narrowed_phrases)
        print(len(narrowed_phrases))
        self.assertEqual(0, len(narrowed_phrases))
        max_phrase, p_list = extract_dates.narrow_phrase_list(phrases, output_dir, just_max=True)
        self.assertEqual(1, len(max_phrase))
