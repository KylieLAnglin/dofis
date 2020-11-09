import pandas as pd
import numpy as np
import pytest

from dofis.data_from_tea.library import clean_teachers


test_data = pd.DataFrame()
test_data['id'] = [1, 2, 3]
test_data['standard'] = [False, True, False]
test_data['cert_area'] = ['A', 'B', 'B']
test_data['cert_level'] = ['low', 'high', 'high']
test_data = test_data.set_index('id')


def test_clean_teachers():
    Aonly = clean_teachers.gen_subject(df=test_data, new_col='test',
                                   area_tuple=('cert_area', 'A'))
    
    assert Aonly.loc[1]['test'] == True


    Bhigh = clean_teachers.gen_subject(df=test_data, new_col='test',
                                       area_tuple=('cert_area', 'B'),
                                       level_tuple=('cert_level', 'high'))

    assert Bhigh.loc[1]['test'] == False
    assert Bhigh.loc[2]['test'] == True


    Bstandard = clean_teachers.gen_subject(df=test_data, new_col='test',
                                           area_tuple=('cert_area', 'B'),
                                           standard_tuple=('standard', True))

    assert Bstandard.loc[1]['test'] == False
    assert Bstandard.loc[2]['test'] == True
    assert Bstandard.loc[3]['test'] == False
