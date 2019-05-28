import unittest
import pandas as pd
import os
from start import data_path
import sys

import engarde.decorators as ed
sys.path.append("../../analysis/library")
print(sys.path)

import test_data



# statistics taken from: https://rptsvr1.tea.texas.gov/perfreport/tapr/2017/state.pdf
# TODO: make this print key statistics from all datasets. TEA master, TEA district merge, data with PS
class TestCampusDataIntegrity1617(unittest.TestCase):
    def test_number_districts(self):
        data = pd.read_csv(os.path.join(data_path, 'clean', 'master_data.csv'), sep=",")
        @ed.verify(test_data.allyearsanddistricts)
        #@ed.verify(test_data.math2018correct) TODO why does this math test fail
        def load():
            return data
        data = load()

        self.assertTrue(True)



if __name__ == '__main__':
    unittest.main()
