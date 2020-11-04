from dofis.merge_and_clean.library import clean_final
import pandas as pd
import numpy as np
import datetime
import pytest

test_data = pd.DataFrame()
test_data['distname'] = ['A', 'B', 'C']
test_data['term_year'] = [2017, 2018, np.nan]
test_data['term_month'] = ['January', np.nan, '']

test_data['finalize_year'] = [2018, 2019, 2019]
test_data['finalize_month'] = ['February', 'September', 'October']


def test_prioritize_term_date():
    dates = clean_final.prioritize_term_date(test_data)
    dates = dates.set_index('distname')

    assert dates.loc['A']['doi_date'] == pd.Timestamp('2017-01-01 00:00:00')
    assert dates.loc['B']['doi_date'] == pd.Timestamp('2018-08-01 00:00:00')
    assert dates.loc['C']['doi_date'] == pd.Timestamp('2019-10-01 00:00:00')
    assert isinstance(dates, pd.DataFrame)


def test_next_month():
    assert 2017 == clean_final.next_month(pd.Timestamp('2017-01-01 00:00:00'),
                                          month=3, day=1)
    assert 2018 == clean_final.next_month(pd.Timestamp('2017-03-02 00:00:00'),
                                          month=3, day=1)
    assert 2018 == clean_final.next_month(pd.Timestamp('2017-03-01 00:00:00'),
                                          month=3, day=1)


