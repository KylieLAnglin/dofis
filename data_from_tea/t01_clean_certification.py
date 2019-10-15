import pandas as pd
import os
import fnmatch
import numpy as np
from data_from_tea.library import start
from data_from_tea.library import clean_tea

###
# Certification
###

year = 'yr1718'

for year in ['yr1213', 'yr1314', 'yr1415', 'yr1516', 'yr1617', 'yr1718']:

    # Files
    folder = 'certification_' + year + '/'
    teacher_datapath = os.path.join(start.data_path, 'tea', 'teachers', folder)

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

    # Rename and keep
    if year > 'yr1415':
        vars_to_keep = {'PERSONID_SCRAM': 'teacher_id', 'DISTRICT': 'district',
                        'CREDENTIAL_TYPE': 'cert_type', 'CERTIFICATE_PREPARATION_ROUTE': 'cert_route',
                        'CERTIFICATION_LEVEL': 'cert_level', 'CREDENTIALED_GRADES': 'cert_grades',
                        'SUBJECT_AREA': 'cert_area', 'SUBJECT': 'cert_subject'}
    else:
        vars_to_keep = {'personid_SCRAM': 'teacher_id', 'DISTRICT': 'district',
                        'CREDENTIAL TYPE': 'cert_type', 'CERTIFICATE PREPARATION ROUTE': 'cert_route',
                        'CERTIFICATION LEVEL': 'cert_level', 'CREDENTIALED GRADES': 'cert_grades',
                        'SUBJECT AREA': 'cert_area', 'SUBJECT': 'cert_subject'}
    certification = clean_tea.filter_and_rename_cols(certification, vars_to_keep)

    # Generate binary certified variable
    cert_types = {'Emergency Non-Certified': False, 'Emergency Certified': False,
                  'Emergency': False, 'Emergency Teaching': False,
                  'Temporary Exemption': False, 'Temporary Teaching Certificate': False,
                  'Unknown Permit': False, 'Unknown': False,
                  'Special Assignment': False,
                  'Paraprofessional': False, 'Standard Paraprofessional': False, 'Non-renewable': False,
                  'Standard': True, 'Provisional': True,
                  'Probationary': True, 'Probationary Extension': True, 'Probationary Second Extension': True,
                   'One Year': True,
                  'Visiting International Teacher': True,
                  'Professional': True, 'Standard Professional': True}
    certification['certification'] = certification['cert_type'].map(cert_types)
    certification['vocational'] = np.where((certification['cert_type'] == "Vocational"), True, False)
    certification.head()

    # Generate binary grades certified variables
    grades_elem = {'Grades EC-4': True, 'Grades EC-6': True, 'Grades EC-12': True,
                   'Grades PK-KG': True, 'Grades PK-3': True, 'Grades PK-5': True, 'Grades PK-12': True,
                   'Grades 1-8': True, 'Grades 1-6': True,
                   'Grades 4-8': True,
                   'Grades 6-8': False, 'Grades 6-10': False, 'Grades 6-12': False,
                   'Grades 7-12': False,
                   'Grades 8-12': False}
    grades_middle = {'Grades EC-4': False, 'Grades EC-6': True, 'Grades EC-12': True,
                     'Grades PK-KG': False, 'Grades PK-3': False, 'Grades PK-5': False, 'Grades PK-12': True,
                     'Grades 1-8': True, 'Grades 1-6': True,
                     'Grades 4-8': True,
                     'Grades 6-8': True, 'Grades 6-10': True, 'Grades 6-12': True,
                     'Grades 7-12': True,
                     'Grades 8-12': True}
    grades_high = {'Grades EC-4': False, 'Grades EC-6': False, 'Grades EC-12': True,
                   'Grades PK-KG': False, 'Grades PK-3': False, 'Grades PK-5': False, 'Grades PK-12': True,
                   'Grades 1-8': False, 'Grades 1-6': False,
                   'Grades 4-8': False,
                   'Grades 6-8': False, 'Grades 6-10': True, 'Grades 6-12': True,
                   'Grades 7-12': True,
                   'Grades 8-12': True}

    certification['cert_elem'] = np.where((certification['cert_level'] == "Elementary"), True, False)

    certification['cert_middle'] = certification['cert_grades'].map(grades_middle)
    certification['cert_middle'] = np.where((certification.certification is False), False, certification.cert_middle)

    certification['cert_high'] = certification['cert_grades'].map(grades_high)
    certification['cert_high'] = np.where((certification.certification is False), False, certification.cert_high)

    # Generate binary area certification variables
    certification['cert_area_elem'] = np.where(certification['cert_area'] == "General Elementary (Self-Contained)",
                                               True, False)
    certification['cert_area_ela'] = np.where(certification['cert_area'] == "English Language Arts", True, False)
    certification['cert_area_math'] = np.where(certification['cert_area'] == "Mathematics", True, False)
    certification['cert_area_sci'] = np.where(certification['cert_area'] == "Science", True, False)
    certification['cert_area_voc'] = np.where(certification['cert_area'] == "Vocational Education", True, False)

    certification['cert_secondary_ela'] = np.where(((certification.cert_level == "Secondary") &
                                                    (certification.cert_area_ela == True )), True, False)
    certification['cert_secondary_math'] = np.where(((certification.cert_level == "Secondary") &
                                                     (certification.cert_area_math  == True)), True, False)
    certification['cert_secondary_sci'] = np.where(((certification.cert_level == "Secondary") &
                                                    (certification.cert_area_sci  == True)), True, False)

    certification = certification[
        certification.district != 'San Antonio']  # three teachers don't link to district number

    # Just keep relevant variables
    certification = certification[['teacher_id', 'district', 'cert_level', 'cert_area', 'certification', 'vocational',
                                   'cert_elem', 'cert_middle', 'cert_high',
                                   'cert_area_elem', 'cert_area_ela', 'cert_area_math', 'cert_area_sci',
                                   'cert_area_voc',
                                   'cert_secondary_ela', 'cert_secondary_math', 'cert_secondary_sci']]

    certification['district'] = certification.district.astype(int)
    certification['certification'] = certification.certification.astype(bool)
    certification['vocational'] = certification.vocational.astype(bool)
    certification['cert_elem'] = certification.cert_elem.astype(bool)
    certification['cert_middle'] = certification.cert_middle.astype(bool)
    certification['cert_high'] = certification.cert_high.astype(bool)
    certification['cert_area_elem'] = certification.cert_area_elem.astype(bool)
    certification['cert_area_ela'] = certification.cert_area_ela.astype(bool)
    certification['cert_area_math'] = certification.cert_area_math.astype(bool)
    certification['cert_area_sci'] = certification.cert_area_sci.astype(bool)
    certification['cert_area_voc'] = certification.cert_area_voc.astype(bool)

    # Save to CSV
    certification.sort_values(by=['teacher_id'], axis=0)
    filename = 'certs_' + year + '.csv'
    certification.to_csv(os.path.join(start.data_path, 'tea', 'teachers', filename))

    # Collapse to teacher level
    teacher_cert = certification[['teacher_id', 'district', 'certification', 'vocational',
                                  'cert_elem', 'cert_middle', 'cert_high',
                                  'cert_area_elem', 'cert_area_ela', 'cert_area_math', 'cert_area_sci', 'cert_area_voc',
                                  'cert_secondary_ela', 'cert_secondary_math', 'cert_secondary_sci']]
    teacher_cert = teacher_cert.groupby(['teacher_id']).max()

    # Save to CSV
    teacher_cert.sort_values(by=['teacher_id'], axis=0)
    filename = 'teacher_cert_' + year + '.csv'
    teacher_cert.to_csv(os.path.join(start.data_path, 'tea', 'teachers', filename))
