import pandas as pd
import os
from data_from_tea.library.start import data_path
from data_from_tea.library import clean_tea

years = [ 'yr1819']
for year in years:
    print(year)
    # distname, campus, campname, campischarter, cntyname_c, grade_range, region, academic rating
    cref = clean_tea.clean_cref(year=year)
    cref = clean_tea.fix_duplicate_distname(cref, distname_col='distname', cntyname_col= 'cntyname_c')

    # add district number and district academic and financial rating
    dref = clean_tea.clean_dref(year=year)
    dref = clean_tea.fix_duplicate_distname(dref, distname_col='distname', cntyname_col= 'cntyname')

    # rural, urbam, suburban
    dtype = clean_tea.clean_dtype(year=year)

    # student and teacher characteristics
    cdem = clean_tea.clean_cdem(year=year)



    # test scores
    cscores = pd.DataFrame(columns=['campus'])

    subjects = ['3rd', '4th', '5th', '6th', '7th', '8th',
            'Algebra', 'Biology', 'EnglishI', 'EnglishII', 'USHistory']
    for subject in subjects:
        cscores_subject = clean_tea.clean_cscores(year, subject)
        cscores = cscores.merge(cscores_subject, how='outer',
                                on='campus')
    descriptives = cref.merge(dref, on='distname', how='inner')
    descriptives = descriptives.merge(dtype, on='district', how='inner')
    descriptives = descriptives.merge(cdem, on='campus', how='left')
    descriptives = descriptives.merge(cscores, on='campus',
                                      how='left', indicator=True)
    descriptives = descriptives.dropna(how='all')

    # days
    if year == 'yr1617' or year == 'yr1718':
        cdays = clean_tea.clean_cdays(year)
        descriptives = descriptives.merge(cdays, on = 'campus', how = 'left')
        print(len(descriptives))

    year_map = {'yr1112':2012, 'yr1213':2013, 'yr1314':2014, 'yr1415': 2015,
                'yr1516': 2016, 'yr1617': 2017, 'yr1718': 2018, 'yr1819': 2019,
                'yr1920': 2020}
    descriptives['year'] = year_map[year]
    yr_file = 'desc_c_' + year + '.csv'

    descriptives.to_csv((os.path.join(data_path, 'tea', yr_file)))

