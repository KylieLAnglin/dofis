import pandas as pd
import os
try:
    from data_from_tea.library import start
except: 
    from library import start

years = ['yr1213', 'yr1314', 'yr1415', 'yr1516', 'yr1617', 'yr1718']
year = 'yr1718'

for year in years:

    # Certification Data
    file = 'certs_' + year + '.csv'
    certification = pd.read_csv(os.path.join(start.data_path, 'tea', 'teachers', file))
    certification = certification.rename(columns = {'district': 'district_cert'})

    # Teacher Data
    file = 'teachers_' + year + '.csv'
    assignments = pd.read_csv(os.path.join(start.data_path, 'tea', 'teachers', file))
    teachers = assignments.merge(certification, on = ['teacher_id'], how = 'left', indicator = '_merge')
    teachers._merge.value_counts()

    # Teacher and Certification Counts and Percent
    num_teachers = teachers[['district', 'campus', 'teacher_id']].groupby(['district', 'campus']).nunique()
    num_teachers = num_teachers[['teacher_id']].rename(columns = {'teacher_id': 'teachers_num_total'})

    num_certified = teachers[(teachers.certified == True)][['district', 'campus', 'teacher_id']].groupby(['district', 'campus']).nunique()
    num_certified = num_certified[['teacher_id']].rename(columns = {'teacher_id': 'teachers_num_certified'})
    teachers_campus = num_teachers.merge(num_certified, left_index = True, right_index = True, how = 'left')

    num_vocational = teachers[((teachers.vocational == True) & (teachers.certified == False))][['district', 'campus', 'teacher_id']].groupby(['district', 'campus']).nunique()
    num_vocational = num_vocational[['teacher_id']].rename(columns = {'teacher_id': 'teachers_num_vocational'})
    teachers_campus = teachers_campus.merge(num_vocational, left_index = True, right_index = True, how = 'left')

    num_uncertified = teachers[(teachers.certified == False)][['district', 'campus', 'teacher_id']].groupby(['district', 'campus']).nunique()
    num_uncertified = num_uncertified[['teacher_id']].rename(columns = {'teacher_id': 'teachers_num_uncertified'})
    teachers_campus = teachers_campus.merge(num_uncertified, left_index = True, right_index = True, how = 'left')

    num_nocertdata = teachers[(teachers._merge == 'left_only')][['district', 'campus', 'teacher_id']].groupby(['district', 'campus']).nunique()
    num_nocertdata = num_nocertdata[['teacher_id']].rename(columns = {'teacher_id': 'teachers_num_nocertdata'})
    teachers_campus = teachers_campus.merge(num_nocertdata, left_index = True, right_index = True, how = 'left')
    teachers_campus = teachers_campus.fillna(0)

    # Add year variable
    years = {'yr1112': 2012,'yr1213': 2013, 'yr1314': 2014, 'yr1415': 2015, 'yr1516': 2016, 'yr1617':2017, 'yr1718': 2018, 'yr1819': 2019}
    teachers_campus['year'] = years[year]

    # Save
    teachers_campus.to_csv(os.path.join(start.data_path, 'tea', 'teachers', 'teachers_c_' + year + '.csv'))

    # District-Level
    teachers_district = teachers_campus.groupby(['district']).sum()
    teachers_district.to_csv(os.path.join(start.data_path, 'tea', 'teachers',  'teachers_d_' + year + '.csv'))

teachers_c_yr1213 = pd.read_csv((os.path.join(start.data_path, 'tea', 'teachers', 'teachers_c_yr1213.csv')))
teachers_c_yr1314 = pd.read_csv((os.path.join(start.data_path, 'tea', 'teachers', 'teachers_c_yr1314.csv')))
teachers_c_yr1415 = pd.read_csv((os.path.join(start.data_path, 'tea', 'teachers', 'teachers_c_yr1415.csv')))
teachers_c_yr1516 = pd.read_csv((os.path.join(start.data_path, 'tea', 'teachers', 'teachers_c_yr1516.csv')))
teachers_c_yr1617 = pd.read_csv((os.path.join(start.data_path, 'tea', 'teachers', 'teachers_c_yr1617.csv')))
teachers_c_yr1718 = pd.read_csv((os.path.join(start.data_path, 'tea', 'teachers', 'teachers_c_yr1718.csv')))

teachers_c_long = pd.concat([teachers_c_yr1213, teachers_c_yr1314, teachers_c_yr1415, teachers_c_yr1516, teachers_c_yr1617, teachers_c_yr1718], sort = True)
teachers_c_long.to_csv((os.path.join(start.data_path, 'tea', 'teachers_c_long.csv')))

teachers_d_yr1213 = pd.read_csv((os.path.join(start.data_path, 'tea', 'teachers', 'teachers_d_yr1213.csv')))
teachers_d_yr1314 = pd.read_csv((os.path.join(start.data_path, 'tea', 'teachers', 'teachers_d_yr1314.csv')))
teachers_d_yr1415 = pd.read_csv((os.path.join(start.data_path, 'tea', 'teachers', 'teachers_d_yr1415.csv')))
teachers_d_yr1516 = pd.read_csv((os.path.join(start.data_path, 'tea', 'teachers', 'teachers_d_yr1516.csv')))
teachers_d_yr1617 = pd.read_csv((os.path.join(start.data_path, 'tea', 'teachers', 'teachers_d_yr1617.csv')))
teachers_d_yr1718 = pd.read_csv((os.path.join(start.data_path, 'tea', 'teachers', 'teachers_d_yr1718.csv')))

teachers_d_long = pd.concat([teachers_d_yr1213, teachers_d_yr1314, teachers_d_yr1415, teachers_d_yr1516, teachers_d_yr1617, teachers_d_yr1718], sort = True)

teachers_d_long.to_csv((os.path.join(start.data_path, 'tea', 'teachers_d_long.csv')))
