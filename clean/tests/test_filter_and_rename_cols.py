
from unittest import TestCase
from clean import clean_tea
import pandas as pd
import numpy as np

class TestFilter_and_ename_cols(TestCase):
    def test_filter_and_rename_cols(self):
        df = pd.DataFrame(np.random.randint(low=0, high=10, size=(5, 5)), columns = ['a', 'b', 'c', 'd', 'e'])
        dict = {'a': 'aa', 'b': 'bb', 'c': 'cc'}
        test = clean_tea.filter_and_rename_cols(df, dict)
        result = list(test.columns)
        self.assertEqual('aa', result[0])
        self.assertEqual(3, len(result))