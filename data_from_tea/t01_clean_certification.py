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
#for year in ['yr1718']:

# Files
folder = 'certification_' + year + '/'
teacher_datapath = os.path.join(start.data_path, 'tea', 'teachers', folder)

pattern = "CERTIFICATION*.csv"
if year == 'yr1213' or year == 'yr1314':
    pattern = "CERTIFICATION*.TXT"

cert = build.concat_files(path=teacher_datapath, pattern=pattern)

# Rename and keep
if year > 'yr1415':
    vars_to_keep = {'PERSONID_SCRAM': 'teacher_id', 'DISTRICT': 'district',
                    'ROLE_CREDENTIALED_FOR': 'role',
                    'CREDENTIAL_TYPE': 'cert_type',
                    'CERTIFICATE_PREPARATION_ROUTE': 'cert_route',
                    'CERTIFICATE_EXPIRATION_DATE': 'expiration',
                    'CERTIFICATION_LEVEL': 'cert_level',
                    'CREDENTIALED_GRADES': 'cert_grades',
                    'SUBJECT_AREA': 'cert_area',
                    'SUBJECT': 'cert_subject'}
else:
    vars_to_keep = {'personid_SCRAM': 'teacher_id', 'DISTRICT': 'district', 
                    'ROLE_CREDENTIALED FOR': 'role',
                    'CERTIFICATE EXPIRATION DATE': 'expiration',
                    'CREDENTIAL TYPE': 'cert_type',
                    'CERTIFICATE PREPARATION ROUTE': 'cert_route',
                    'CERTIFICATION LEVEL': 'cert_level',
                    'CREDENTIALED GRADES': 'cert_grades',
                    'SUBJECT AREA': 'cert_area',
                    'SUBJECT': 'cert_subject'}
cert = clean_tea.filter_and_rename_cols(cert, vars_to_keep)

# Keep only teachers
cert = cert[cert.role == 'Teacher']

# Grades
cert = clean_teachers.clean_grades(df=cert, col='cert_grades')
cert = clean_teachers.split_grades(df=cert, col='cert_grades',
                                    low_name='cert_grade_low',
                                    high_name='cert_grade_high')

# Expiration
cert['expiration'] = cert['expiration'].str[0:9]
cert['expiration'] = pd.to_datetime(
    cert['expiration'], errors='coerce')

timestamps = {'yr1213': '2012-07-01', 'yr1314': '2013-07-01', 'yr1415': '2014-07-01', 'yr1516': '2015-07-01',
                'yr1617': '2016-07-01', 'yr1718': '2017-07-01', 'yr1819': '2017-0701'}
cert['expired'] = np.where(
    cert.expiration < pd.Timestamp(timestamps[year]), True, False)

# Only keep unexpired
cert = cert[cert.expired == False]



# Create certification variable
cert_types = {'Emergency Non-Certified': False, 'Emergency Certified': True,
                'Emergency': False, 'Emergency Teaching': False,
                'Temporary Exemption': True, 'Temporary Teaching Certificate': False,
                'Unknown Permit': False, 'Unknown': False,
                'Special Assignment': True,
                'Paraprofessional': False, 'Standard Paraprofessional': False, 'Non-renewable': False,
                'Standard': True, 'Provisional': True,
                'Probationary': True, 'Probationary Extension': True, 'Probationary Second Extension': True,
                'One Year': True,
                'Visiting International Teacher': True,
                'Professional': True, 'Standard Professional': True}
cert['certified'] = cert['cert_type'].map(cert_types)

cert['vocational'] = np.where(
    (cert['cert_type'] == "Vocational"), True, False)

cert_types_tea_report = {'Emergency Non-Certified': False, 'Emergency Certified': True,
                            'Emergency': False, 'Emergency Teaching': False,
                            'Temporary Exemption': True, 'Temporary Teaching Certificate': False,
                            'Unknown Permit': False, 'Unknown': False,
                            'Special Assignment': True,
                            'Paraprofessional': False, 'Standard Paraprofessional': False, 'Non-renewable': False,
                            'Standard': True, 'Provisional': True,
                            'Probationary': True, 'Probationary Extension': True, 'Probationary Second Extension': True,
                            'One Year': True,
                            'Visiting International Teacher': True}
cert['certified_report'] = cert['cert_type'].map(
    cert_types_tea_report)

# Generate binary grades certified variables. True if certified for any grades
area = {'General Elementary (Self-Contained)': 'elem', 'Bilingual Education': 'biling', 'English Language Arts': 'ela',
        'Special Education': 'sped', 'Health and Physical Education': 'pe', 'Social Studies': 'ss', 'Mathematics': 'math',
        'Science': 'science', 'Vocational Education': 'voc', 'Fine Arts': 'art', 'Foreign Language': 'for',
        'Computer Science': 'cs', 'Other': 'other'}

# Elementary
cert['cert_area_elem'] = np.where(cert['cert_area'] == "elem",
                                            True, False)
cert['cert_area_elem'] = np.where((cert['cert_area'] == "biling") &
                                            ((cert['cert_level'] == "Elementary") |
                                            (cert['cert_level'] == "All Level")), True, cert.cert_area_elem)
cert['cert_area_elem'] = np.where((cert['cert_area'] == "spend") &
                                            ((cert['cert_level'] == "Elementary") |
                                            (cert['cert_level'] == "All Level")),
                                            True, cert.cert_area_elem)
# Math
cert['cert_area_high_math'] = np.where(cert['cert_area'] == "math",
                                                True, False)
cert['cert_area_high_math'] = np.where(cert.cert_grade_high > 8,
                                                cert.cert_area_high_math, False)

# Science
cert['cert_area_high_science'] = np.where(cert['cert_area'] == "science",
                                                    True, False)
cert['cert_area_high_science'] = np.where(cert.cert_grade_high > 8,
                                                    cert.cert_area_high_math, False)

# three teachers don't link to district number
cert = cert[cert.district != 'San Antonio']

###
# Create any certification dataframe
###

teacher_yesno = cert[['teacher_id', 'district', 'certified', 'vocational',
                                'cert_area_elem', 'cert_area_high_math']]
teacher_yesno = teacher_yesno.groupby(['teacher_id']).max()

# Reshape long to wide
df = cert[['teacher_id', 'district',
                    'cert_area', 'cert_subject',
                    'cert_grade_low', 'cert_grade_high']]
df['idx'] = df.groupby('teacher_id').cumcount()
certs = cert[['teacher_id', 'certified',
                        'vocational']].groupby('teacher_id').max()
df = df.merge(certs, how='left', on='teacher_id')
df['cert_area_idx'] = 'cert_area_' + df.idx.astype(str)
df['cert_subject_idx'] = 'cert_subject_' + df.idx.astype(str)
df['cert_grade_low_idx'] = 'cert_grade_low_' + df.idx.astype(str)
df['cert_grade_high_idx'] = 'cert_grade_high_' + df.idx.astype(str)

areas = df.pivot(index='teacher_id',
                    columns='cert_area_idx', values='cert_area')
subjects = df.pivot(index='teacher_id',
                    columns='cert_subject_idx', values='cert_subject')
low_grades = df.pivot(
    index='teacher_id', columns='cert_grade_low_idx', values='cert_grade_low')
high_grades = df.pivot(
    index='teacher_id', columns='cert_grade_high_idx', values='cert_grade_high')

teacher_cert_wide = pd.concat(
    [areas, subjects, low_grades, high_grades], axis=1)
max_certs = len(list(teacher_cert.filter(regex=("cert_area"))))
variables = []
for num in range(0, max_certs):
    string = '_' + str(num) + '$'
    variables = variables + list(areas.filter(regex=(string)))
    variables = variables + list(subjects.filter(regex=(string)))
    variables = variables + list(low_grades.filter(regex=(string)))
    variables = variables + list(high_grades.filter(regex=(string)))
teacher_cert_wide = teacher_cert_wide[variables]

teacher_cert = teacher_yesno.merge(
    teacher_cert_wide, left_index=True, right_index=True)

# Save to CSV
filename = 'certs_' + year + '.csv'
cert.to_csv(os.path.join(
    start.data_path, 'tea', 'teachers', filename))

# Collapse to teacher level
#teacher_cert = teacher_cert.groupby(['teacher_id']).max()

# Save to CSV
#teacher_cert.sort_values(by=['teacher_id'], axis=0)
#filename = 'teacher_cert_' + year + '.csv'
#teacher_cert.to_csv(os.path.join(start.data_path, 'tea', 'teachers', filename))
