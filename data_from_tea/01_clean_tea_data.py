import pandas as pd
import os

from library import clean_tea
from library.start import data_path

years =  ['yr1112', 'yr1213', 'yr1314', 'yr1415', 'yr1516', 'yr1617', 'yr1718', 'yr1819']
subjects = ['3rd', '4th', '5th', '6th', '7th', '8th',
                'Algebra', 'Biology', 'EnglishI', 'EnglishII', 'USHistory']
for year in years:
    cref = clean_tea.clean_cref(year=year)
    cref = cref[['distname', 'campus']].groupby(['distname']).nunique()
    cref = cref[['campus']].rename(columns = {'campus': 'num_schools'})
    dref = clean_tea.clean_dref(year=year)
    dref = dref.merge(cref, on = 'distname', how = 'left')
    dref = clean_tea.fix_duplicate_distname(dref, distname_col='distname', cntyname_col= 'cntyname')

    ddem = clean_tea.clean_ddem(year=year)
    dtype = clean_tea.clean_dtype(year =year)
    dscores = pd.DataFrame(columns=['district'])
    for subject in subjects:
        dscores_subject  = clean_tea.clean_scores(year, subject)
        dscores = dscores.merge(dscores_subject, how='outer',
                                on='district')
    descriptives = ddem.merge(dref, on='district', how='inner')
    descriptives = descriptives.merge(dtype, on='district', how='left')
    descriptives = descriptives.merge(dscores, on='district',
                                      how='left', indicator=True)
    descriptives = descriptives.dropna(how='all')
    
    print(len(descriptives))

    year_map = {'yr1112':2012, 'yr1213':2013, 'yr1314':2014, 'yr1415': 2015,
                'yr1516': 2016, 'yr1617': 2017, 'yr1718': 2018, 'yr1819': 2019,
                'yr1920': 2020}
    descriptives['year'] = year_map[year]
    yr_file = 'desc_' + year + '.csv'

    descriptives.to_csv((os.path.join(data_path, 'tea', yr_file )))
