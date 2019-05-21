import pandas as pd
import os
from library.start import data_path
from library import clean_tea
from library import clean_tea_schools


years =  ['yr1112', 'yr1213', 'yr1314', 'yr1415', 'yr1516', 'yr1617', 'yr1718']
subjects = ['3rd', '4th', '5th', '6th', '7th', '8th',
                'Algebra', 'Biology', 'EnglishI', 'EnglishII', 'USHistory']
for year in years:
    cref = clean_tea.clean_cref_numschools(year=year)
    cref = clean_tea_schools.fix_duplicate_distname(cref, distname_col='distname', cntyname_col= 'cntyname')
    cref = cref[['distname', 'schools_num']]
    # don't need countyname in both cref and dref)
    dref = clean_tea.clean_dref(year=year)
    dref = clean_tea_schools.fix_duplicate_distname(dref, distname_col='distname', cntyname_col= 'cntyname')

    ddem = clean_tea.clean_ddem(year=year)
    dtype = clean_tea.clean_dtype(year =year)
    dscores = pd.DataFrame(columns=['district'])
    for subject in subjects:
        dscores_subject  = clean_tea.clean_scores(year, subject)
        dscores = dscores.merge(dscores_subject, how='outer',
                                on='district')
    descriptives = ddem.merge(dref, on='district', how='inner')
    descriptives = descriptives.merge(dtype, on='district', how='left')
    descriptives = descriptives.merge(cref, on = 'distname', how = 'inner')
    descriptives = descriptives.merge(dscores, on='district',
                                      how='left', indicator=True)
    descriptives = descriptives.dropna(how='all')
    if year == 'yr1617' or year == 'yr1718':
        ddays = clean_tea.clean_ddays(year)
        descriptives = descriptives.merge(ddays, on = 'district', how = 'left')
        print(len(descriptives))

    year_map = {'yr1112':2012, 'yr1213':2013, 'yr1314':2014, 'yr1415': 2015,
                'yr1516': 2016, 'yr1617': 2017, 'yr1718': 2018, 'yr1819': 2019,
                'yr1920': 2020}
    descriptives['year'] = year_map[year]
    yr_file = 'desc_' + year + '.csv'

    descriptives.to_csv((os.path.join(data_path, 'tea', yr_file )))
