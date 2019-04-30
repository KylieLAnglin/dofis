import pandas as pd
import os
from library.start import data_path
from library import clean_tea_schools
from library import clean_tea

years = ['yr1112', 'yr1213', 'yr1314', 'yr1415', 'yr1516', 'yr1617', 'yr1718']
subjects = ['3rd', '4th', '5th', '6th', '7th', '8th',
            'Algebra', 'Biology', 'EnglishI', 'EnglishII', 'USHistory']
for year in years:

    cref = clean_tea_schools.clean_cref(year=year)
    cref = clean_tea_schools.fix_duplicate_distname(cref, distname_col='distname', cntyname_col= 'cntyname_c')

    dref = clean_tea.clean_dref(year=year)
    dref = clean_tea_schools.fix_duplicate_distname(dref, distname_col='distname', cntyname_col= 'cntyname')

    dtype = clean_tea.clean_dtype(year=year)
    cdem = clean_tea_schools.clean_cdem(year=year)
    cscores = pd.DataFrame(columns=['campus'])
    for subject in subjects:
        cscores_subject = clean_tea_schools.clean_cscores(year, subject)
        cscores = cscores.merge(cscores_subject, how='outer',
                                on='campus')
    descriptives = cref.merge(dref, on='distname', how='inner')
    descriptives = descriptives.merge(dtype, on='district', how='inner')
    descriptives = descriptives.merge(cdem, on='campus', how='left')
    descriptives = descriptives.merge(cscores, on='campus',
                                      how='left', indicator=True)
    descriptives = descriptives.dropna(how='all')

    year_map = {'yr1112':2012, 'yr1213':2013, 'yr1314':2014, 'yr1415': 2015,
                'yr1516': 2016, 'yr1617': 2017, 'yr1718': 2018, 'yr1819': 2019,
                'yr1920': 2020}
    descriptives['year'] = year_map[year]
    yr_file = 'desc_c_' + year + '.csv'

    descriptives.to_csv((os.path.join(data_path, 'tea', yr_file)))

