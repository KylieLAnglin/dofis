from data_from_tea.library import clean_tea
from unittest import TestCase
import pandas as pd

class TestGet_not_in(TestCase):
    def test_get_not_in(self):
        d1 = {'distname': ['Abbott CISD', 'Hamilton ISD']}
        d2 = {'distname': ['Hamilton ISD', 'Cayuga ISD']}
        df1 = pd.DataFrame(data=d1)
        df2 = pd.DataFrame(data=d2)
        result = clean_tea.get_not_in(df1, 'distname', df2, 'distname')
        self.assertEqual(1, len(result))
        self.assertEqual('Abbott CISD', result.distname.values[0])
