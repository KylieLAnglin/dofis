import pandas as pd
import os
import fnmatch
import numpy as np
import datetime

from dofis.data_from_tea.library import start
from dofis.data_from_tea.library import clean_tea
from dofis.data_from_tea.library import build
from dofis.data_from_tea.library import clean_teachers


pd.set_option('display.max_columns', None)

###
# Certification
###

year = 'yr1718'
years = ['yr1213', 'yr1314', 'yr1415', 'yr1516', 'yr1617', 'yr1718']
for year in years:

    # Files
    teacher_datapath = os.path.join(start.data_path, 'teachers', year)

    pattern = 'CERTIFICATION_*.csv'
    if year == 'yr1213' or year == 'yr1314':
        pattern = 'CERTIFICATION*.TXT'

    cert = build.concat_files(path=teacher_datapath, pattern=pattern)

    # Rename and keep
    if year > 'yr1415':
        vars_to_keep = {'PERSONID_SCRAM': 'teacher_id', 'DISTRICT': 'district',
                        'ROLE_CREDENTIALED_FOR': 'role',
                        'CREDENTIAL_TYPE': 'cert_type',
                        'CERTIFICATE_EXPIRATION_DATE': 'expiration',
                        'CERTIFICATION_LEVEL': 'cert_level',
                        'SUBJECT_AREA': 'cert_area',
                        'SUBJECT': 'cert_subject'}
    else:
        vars_to_keep = {'personid_SCRAM': 'teacher_id', 'DISTRICT': 'district',
                        'ROLE_CREDENTIALED FOR': 'role',
                        'CERTIFICATE EXPIRATION DATE': 'expiration',
                        'CREDENTIAL TYPE': 'cert_type',
                        'CERTIFICATION LEVEL': 'cert_level',
                        'SUBJECT AREA': 'cert_area'}

    cert = clean_tea.filter_and_rename_cols(cert, vars_to_keep)

    # Keep only teachers
    cert = cert[cert.role == 'Teacher']

    # generate certification variables
    cert = clean_teachers.gen_standard_certification(df=cert,
                                                     col='cert_type',
                                                     new_var='standard')

    cert = clean_teachers.gen_subject(df=cert, new_col='cert_area_math',
                                      area_tuple=('cert_area', 'Mathematics'),
                                      standard_tuple=('standard', True))

    cert = clean_teachers.gen_subject(df=cert, new_col='cert_area_math_high',
                                      area_tuple=('cert_area', 'Mathematics'),
                                      level_tuple=('cert_level', 'Secondary'),
                                      standard_tuple=('standard', True))

    cert = clean_teachers.gen_subject(df=cert, new_col='cert_area_science',
                                      area_tuple=('cert_area', 'Science'),
                                      standard_tuple=('standard', True))

    cert = clean_teachers.gen_subject(df=cert, new_col='cert_area_science_high',
                                      area_tuple=('cert_area', 'Science'),
                                      level_tuple=('cert_level', 'Secondary'),
                                      standard_tuple=('standard', True))

    # three teachers don't link to district number
    cert = cert[cert.district != 'San Antonio']

    ###
    # Create any certification dataframe
    ###

    # Any standard certification? (Includes alternative certification)
    teacher_yesno = cert[['teacher_id', 'district', 'standard',
                          'cert_area_math', 'cert_area_math_high',
                          'cert_area_science', 'cert_area_science_high']]

    teacher_yesno = teacher_yesno.groupby(['teacher_id']).max()

    # Save to CSV
    filename = 'teacher_cert_' + year + '.csv'
    teacher_yesno.to_csv(os.path.join(
        start.data_path, 'teachers', filename))
