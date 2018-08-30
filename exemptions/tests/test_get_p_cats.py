from unittest import TestCase
from exemptions import extract_dates
import os
from exemptions import start

class TestGet_p_cats(TestCase):
    def test_get_p_cats(self):
        test = ['meets to draft Innovation Plan March 2, 2017 March DOI meets to draft',
                'Introduction House Bill 1842, passed during the 84th Legislative Session']
        output_dir = os.path.join(start.data_path, 'date_finalize_classifier')
        p_cat = extract_dates.get_p_cats(test, output_dir)
        first = p_cat[0]['FINALIZE']
        second = p_cat[1]['FINALIZE']
        print(first)
        self.assertLess(.5, first)
        self.assertGreater(.5, second)

        test2 = ['hello']
        p_cat = extract_dates.get_p_cats(test2, output_dir)
        third = p_cat[0]['FINALIZE']
        print(third)
        self.assertGreater(.5, third)
