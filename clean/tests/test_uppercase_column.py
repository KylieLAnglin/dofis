from unittest import TestCase
from clean.library import clean_exemptions
import pandas as pd

class TestUppercase_column(TestCase):
    def test_uppercase_column(self):
        d = {'distname': ['Abbott ISD']}
        df = pd.DataFrame(data=d)
        df = clean_exemptions.uppercase_column(df, 'distname')
        result = df[df.distname.str.startswith('A')]['distname'].values[0]
        self.assertEqual('ABBOTT ISD', result)
