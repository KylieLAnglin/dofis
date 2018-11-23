import pandas as pd
import os
from library.start import data_path
from library import clean_tea_schools


years =  ['yr1112', 'yr1213', 'yr1314', 'yr1415', 'yr1516', 'yr1617', 'yr1718']
subjects = ['3rd', '4th', '5th', '6th', '7th', '8th',
                'Algebra', 'Biology', 'EnglishI', 'EnglishII', 'USHistory']
for year in years:

    cref = clean_tea_schools.clean_cref(year=year)
    cdem = clean_tea_schools.clean_cdem(year=year)
    cscores = pd.DataFrame(columns=['campus'])
    for subject in subjects:
        cscores_subject = clean_tea_schools.clean_cscores(year, subject)
        cscores = cscores.merge(cscores_subject, how='outer',
                                on='campus')
    descriptives = cdem.merge(cref, on='campus', how='inner')
    descriptives = descriptives.merge(cscores, on='campus',
                                      how='left', indicator=True)
    descriptives = descriptives.dropna(how='all')

    descriptives['year'] = year
    yr_file = 'desc_c_' + year + '.csv'

    descriptives.to_csv((os.path.join(data_path, 'tea', yr_file )))

    print(data_path, "one down")
