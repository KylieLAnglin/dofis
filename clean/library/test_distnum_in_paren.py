from unittest import TestCase
from clean.library import clean_exemptions
import pandas as pd

class TestDistnum_in_paren(TestCase):
    def test_distnum_in_paren(self):
        d = {'distname': ['CAYUGA ISD'], 'district': ['1902']}
        df = pd.DataFrame(data=d)
        df = clean_exemptions.distnum_in_paren(df)
        result = df[df.distname.str.startswith('C')]['distname'].values[0]
        self.assertEqual('CAYUGA ISD (001902)', result)
