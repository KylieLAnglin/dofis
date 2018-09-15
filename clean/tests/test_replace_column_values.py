from unittest import TestCase
from clean.library import clean_for_merge
import pandas as pd

class TestReplace_column_values(TestCase):
    def test_replace_column_values(self):
        d = {'distname': ['Abbott CISD']}
        df = pd.DataFrame(data=d)
        df = clean_for_merge.replace_column_values(df, 'distname', 'CISD', 'ISD')
        result = df[df.distname.str.startswith('A')]['distname'].values[0]
        self.assertEqual('Abbott ISD', result)

