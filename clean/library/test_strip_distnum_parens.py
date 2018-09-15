from unittest import TestCase
from clean.library import clean_for_merge
import pandas as pd

class TestStrip_distnum_parens(TestCase):
    def test_strip_distnum_parens(self):
        str_list = ['CENTERVILLE ISD (145902)',
                     'CENTERVILLE ISD (228904)',
                     'CHAPEL HILL ISD (225906)',
                     'EDGEWOOD ISD (015905)',
                     'EDGEWOOD ISD (234903)',
                     'HIGHLAND PARK ISD (057911)',
                     'HIGHLAND PARK ISD (188903)',
                     'HUBBARD ISD (019913)',
                     'HUBBARD ISD (109905)',
                     'MIDWAY ISD (161903)',
                     'NORTHSIDE ISD (244905)',
                     'WYLIE ISD (043914)',
                     'WYLIE ISD (221912)']
        result = clean_for_merge.strip_distnum_parens(str_list)
        self.assertEqual('CENTERVILLE ISD', result[0])