import os

import numpy as np
import pandas as pd

from library import start


no_cert_merge = 'missing'

years = ['yr1213', 'yr1314', 'yr1415', 'yr1516', 'yr1617', 'yr1718']
for year in years:

    filename = 'teacher_cert_' + year + '.csv'
    certification = pd.read_csv(os.path.join(
        start.data_path, 'teachers', filename))
    certification = certification.rename(columns={'district': 'district_cert'})

    filename = 'teachers_' + year + '.csv'
    teachers = pd.read_csv(os.path.join(start.data_path, 'teachers', filename))

    teachers = teachers.merge(certification, how='left',
                              on='teacher_id', indicator='cert_merge')
    
    if no_cert_merge == 'uncertified':
        for var in ['standard', 'cert_area_math', 'cert_area_math_high',
                    'cert_area_science', 'cert_area_science_high']:
            teachers[var] = np.where(teachers.cert_merge == 'left_only', 0,
                                     teachers[var])


    # Standard Certification
    any_cert = teachers[['campus', 'standard']]
    any_cert = any_cert.groupby(['campus']).mean()
    any_cert = any_cert.rename(columns={'standard': 'certified'})

    count = teachers.groupby(['campus']).count()
    count = count.rename(columns={'standard': 'teacher_count'})
    count = count[['teacher_count']]

    any_cert = any_cert.merge(count, on = 'campus')

    # Add year variable
    years = {'yr1112': 2012, 'yr1213': 2013, 'yr1314': 2014, 'yr1415': 2015,
             'yr1516': 2016, 'yr1617': 2017, 'yr1718': 2018, 'yr1819': 2019}
    any_cert['year'] = years[year]

    # Save
    filename = 'campus_cert_' + year + '.csv'
    any_cert.to_csv(os.path.join(start.data_path, 'teachers', filename))


###
#   Append
###

certification_rates_yr1213 = pd.read_csv(
    (os.path.join(start.data_path, 'teachers', 'campus_cert_yr1213.csv')))
certification_rates_yr1314 = pd.read_csv(
    (os.path.join(start.data_path, 'teachers', 'campus_cert_yr1314.csv')))
certification_rates_yr1415 = pd.read_csv(
    (os.path.join(start.data_path, 'teachers', 'campus_cert_yr1415.csv')))
certification_rates_yr1516 = pd.read_csv(
    (os.path.join(start.data_path, 'teachers',  'campus_cert_yr1516.csv')))
certification_rates_yr1617 = pd.read_csv(
    (os.path.join(start.data_path, 'teachers',  'campus_cert_yr1617.csv')))
certification_rates_yr1718 = pd.read_csv(
    (os.path.join(start.data_path, 'teachers',  'campus_cert_yr1718.csv')))

certification_rates_long = pd.concat([certification_rates_yr1213,
                                      certification_rates_yr1314,
                                      certification_rates_yr1415,
                                      certification_rates_yr1516,
                                      certification_rates_yr1617,
                                      certification_rates_yr1718], sort=True)

certification_rates_long.to_csv(
    (os.path.join(start.data_path, 'tea', 'certification_rates_long.csv')))
