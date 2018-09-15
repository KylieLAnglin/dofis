import pandas as pd
import clean
import os
from start import data_path
import csv


years =  ['yr1112', 'yr1213', 'yr1314', 'yr1415', 'yr1516', 'yr1617', 'yr1718']
subjects = ['3rd', '4th', '5th', '6th', '7th', '8th',
                'Algebra', 'Biology', 'EnglishI', 'EnglishII', 'USHistory']
for year in years:

    dref = clean.clean_dref(year=year)
    ddem = clean.clean_ddem(year=year)
    dscores = pd.DataFrame(columns=['district'])
    for subject in subjects:
        dscores_subject = clean.clean_scores(year, subject)
        dscores = dscores.merge(dscores_subject, how='outer',
                                on='district')
    descriptives = ddem.merge(dref, on='district', how='inner')
    descriptives = descriptives.merge(dscores, on='district',
                                      how='left', indicator=True)
    descriptives = descriptives.dropna(how='all')

    dscores['year'] = year
    yr_file = 'desc_' + year + '.csv'

    dscores.to_csv((os.path.join(data_path, yr_file )))
    