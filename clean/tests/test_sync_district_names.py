from unittest import TestCase
from clean.library import clean_exemptions
import pandas as pd

class TestSync_district_names(TestCase):
    def test_sync_district_names(self):
        d = {'distname': ['EAGLE MT-SAGINAW ISD']}
        df = pd.DataFrame(data=d)
        df = clean_exemptions.sync_district_names(df, 'distname')
        result = df[df.distname.str.startswith('E')]['distname'].values[0]
        self.assertEqual('EAGLE MOUNTAIN SAGINAW ISD', result)
