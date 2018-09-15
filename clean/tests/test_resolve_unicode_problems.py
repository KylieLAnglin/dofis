from unittest import TestCase
from clean.library import clean_exemptions
import pandas as pd

class TestResolve_unicode_problems(TestCase):
    def test_resolve_unicode_problems(self):
        test = 'Bronte\xa0ISD'
        d = {'distname': [test, 'Abbott ISD']}
        df = pd.DataFrame(data=d)
        df = clean_exemptions.resolve_unicode_problems(df, 'distname')
        result = df[df.distname.str.startswith('Bronte')]['distname'].values[0]
        result2 = df[df.distname.str.startswith('Abbott')]['distname'].values[0]
        self.assertEqual('Bronte ISD', result)
        self.assertEqual('Abbott ISD', result2)

