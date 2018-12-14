import pandas as pd
import os
import fnmatch
import numpy as np
from library import start
from library import clean_tea

year_list = ['yr1213', 'yr1314', 'yr1415', 'yr1516', 'yr1617', 'yr1718']
for year in year_list:

    folder = 'certification_' + year + '/'
    teacher_datapath = os.path.join(start.data_path, 'tea', 'teachers', folder)
    # # #
    # Certification
    # # #
    # Append all certification data sets from 2016-17
    pattern = "CERTIFICATION*.csv"
    if year == 'yr1213' or year == 'yr1314':
        pattern = "CERTIFICATION*.TXT"
    cert_files = []
    for entry in os.listdir(teacher_datapath):
        if fnmatch.fnmatch(entry, pattern):
            cert_files.append(entry)
    cert_files.sort()
    dirs_cert = [teacher_datapath + file for file in cert_files]
    df_list = [pd.read_csv(file, sep=",", encoding="ISO-8859-1", dtype=object) for file in dirs_cert]
    certification = pd.concat(df_list)

    vars_to_keep = {'PERSONID_SCRAM': 'teacher_id', 'DISTRICT': 'district',
                    'CREDENTIAL TYPE': 'cert_type', 'CERTIFICATE_PREPARATION_ROUTE': 'cert_route',
                    'CERTIFICATE LIFE': 'cert_life',
                    'CERTIFICATE EFFECTIVE DATE': 'cert_startdate', 'CERTIFICATE EXPIRATION DATE': 'cert_enddate',
                    'CERTIFICATION_LEVEL': 'cert_level', 'CREDENTIALED_GRADES': 'cert_grades',
                    'POPULATION_CREDENTIALED_FOR': 'cert_pop',
                    'SUBJECT AREA': 'cert_area', 'SUBJECT': 'cert_subject'}
    if year in ['yr1213', 'yr1314']:
        vars_to_keep = {'personid_SCRAM': 'teacher_id', 'DISTRICT': 'district',
                        'CREDENTIAL TYPE': 'cert_type', 'CERTIFICATE PREPARATION ROUTE': 'cert_route',
                        'CERTIFICATE LIFE': 'cert_life',
                        'CERTIFICATE EFFECTIVE DATE': 'cert_startdate', 'CERTIFICATE EXPIRATION DATE': 'cert_enddate',
                        'CERTIFICATION LEVEL': 'cert_level', 'CREDENTIALED GRADES': 'cert_grades',
                        'POPULATION CREDENTIALED FOR': 'cert_pop',
                        'SUBJECT AREA': 'cert_area', 'SUBJECT': 'cert_subject'}

    certification = clean_tea.filter_and_rename_cols(certification, vars_to_keep)
    cert_vars = list(vars_to_keep.values())
    cert_vars.remove('teacher_id')

    certification = certification.sort_values(by='teacher_id')
    print('number of certifications: ', len(certification), 'in', year)

    # Keep only latest certification of duplicates
    certification['cert_startdate'] = pd.to_datetime(certification.cert_startdate.str.slice(0, 9), errors='coerce')
    certification['cert_enddate'] = np.where(certification['cert_life'] == 'LIFE', '02JAN2050:00:00:00',
                                             certification['cert_enddate'])
    certification['cert_enddate'] = pd.to_datetime(certification.cert_enddate.str.slice(0, 9), errors='coerce')

    cert_vars_dup = []
    for var in cert_vars:
        if var not in ['cert_startdate', 'cert_enddate', 'cert_route']:
            cert_vars_dup.append(var)
    cert_vars_dup.append('teacher_id')
    certification = certification.sort_values(by=cert_vars_dup, ascending=True)
    certification = certification.drop_duplicates(subset=cert_vars_dup, keep='last')

    # create certification count within each scrabled id
    certification['idx'] = certification.groupby('teacher_id').cumcount()
    print('some teachers have as many as ', certification.idx.max(), 'current certifications')
    print(certification[certification.idx > 15].teacher_id.nunique(),
          'have over 15. We will drop some of these certification for readbility.',
          'Since it is so small a number it shouldnt impact estimates.')
    certification = certification[certification.idx <= 15]

    # Need to reshape for merge so that each teacher is a single row.
    certification_wide = certification.pivot(index='teacher_id', columns='idx')[cert_vars]
    cols = certification_wide.columns
    ind = pd.Index([e[0] + str(e[1]) for e in cols.tolist()])
    certification_wide.columns = ind

    # # #
    # Teachers
    # # #
    pattern = "TEACHER_MASTER*.TXT"
    teacher_files = []
    for entry in os.listdir(teacher_datapath):
        if fnmatch.fnmatch(entry, pattern):
            teacher_files.append(entry)
    teacher_files.sort()
    dirs_teachers = [teacher_datapath + file for file in teacher_files]
    df_list = [pd.read_csv(file, sep=",", encoding="ISO-8859-1", dtype=object) for file in dirs_teachers]
    teachers = pd.concat(df_list)

    if year in ['yr1213', 'yr1314', 'yr1415', 'yr1516', 'yr1617', 'yr1718']:
        vars_to_keep = {'SCRAMBLED UNIQUE ID': 'teacher_id', 'DISTRICT NUMBER': 'district', 'DISTRICT NAME': 'distname',
                        'CAMPUS NUMBER': 'campus', 'CAMPUS NAME': 'campname', 'FTE': 'fte',
                        'SUBJECT AREA NAME 1': 'sub_area1', 'SUBJECT AREA NAME 2': 'sub_area2',
                        'SUBJECT AREA NAME 3': 'sub_area3',
                        'SUBJECT AREA NAME 4': 'sub_area4', 'SUBJECT AREA NAME 5': 'sub_area5'}
    teacher_vars = list(vars_to_keep.values())
    teachers = clean_tea.filter_and_rename_cols(teachers, vars_to_keep)

    teachers['fte'] = teachers['fte'].apply(pd.to_numeric, errors='coerce')
    teachers = teachers.set_index('teacher_id')

    # # #
    # Merge
    # # #

    teachers_cert = teachers.merge(certification_wide, how='left', left_index=True,
                          right_index=True, indicator=True)
    print(len(teachers_cert[teachers_cert._merge == 'left_only']), 'uncertified teachers in', year)

    filename = 'teachers_' + year + '.csv'
    teachers_cert.to_csv(os.path.join(start.data_path, 'clean', 'teachers', filename),
                sep=",")

# Append
files = []
for year in year_list:
    filename = 'teachers_' + year + '.csv'
    files.append(filename)
df_list = [pd.read_csv(file, sep=",", encoding="ISO-8859-1", dtype=object) for file in files]
teachers_final = pd.concat(df_list)
teachers_final.to_csv(os.path.join(start.data_path, 'clean', 'teachers_final.csv'))
