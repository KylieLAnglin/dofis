from unittest import TestCase
from clean.library import clean_for_merge
import pandas as pd

class TestDistnum_in_paren(TestCase):
    def test_distnum_in_paren(self):
        d = {'distname': ['CAYUGA ISD'], 'district': ['1902']}
        df = pd.DataFrame(data=d)
        result = clean_for_merge.distnum_in_paren(df)
        print(result)
        result = df[df.distname.str.startswith('C')]['distname'].values[0]
        self.assertEqual('CAYUGA ISD (001902)', result)
