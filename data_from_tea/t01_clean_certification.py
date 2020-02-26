import pandas as pd
import os
import fnmatch
import numpy as np
import datetime
try:
    from data_from_tea.library import start
    from data_from_tea.library import clean_tea
except:
    from library import start
    from library import clean_tea  
pd.set_option('display.max_columns', None)

###
# Certification
###

year = 'yr1718'

for year in ['yr1213', 'yr1314', 'yr1415', 'yr1516', 'yr1617', 'yr1718']:

    # Concatenate Files for Year
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

    # Rename and Keep
    if year > 'yr1415':
        vars_to_keep = {'PERSONID_SCRAM': 'teacher_id', 'DISTRICT': 'district', 'ROLE_CREDENTIALED_FOR': 'role',
                        'CREDENTIAL_TYPE': 'cert_type', 'CERTIFICATE_PREPARATION_ROUTE': 'cert_route',
                        'CERTIFICATE_EXPIRATION_DATE': 'expiration',
                        'CERTIFICATION_LEVEL': 'cert_level', 'CREDENTIALED_GRADES': 'cert_grades',
                        'SUBJECT_AREA': 'cert_area', 'SUBJECT': 'cert_subject'}
    else:
        vars_to_keep = {'personid_SCRAM': 'teacher_id', 'DISTRICT': 'district', 'ROLE_CREDENTIALED FOR': 'role',
                        'CERTIFICATE EXPIRATION DATE': 'expiration',
                        'CREDENTIAL TYPE': 'cert_type', 'CERTIFICATE PREPARATION ROUTE': 'cert_route',
                        'CERTIFICATION LEVEL': 'cert_level', 'CREDENTIALED GRADES': 'cert_grades',
                        'SUBJECT AREA': 'cert_area', 'SUBJECT': 'cert_subject'}
    certification = clean_tea.filter_and_rename_cols(certification, vars_to_keep)

    # Code for low- and high-grades certified to teach
    certification['cert_grades'] = certification['cert_grades'].replace({'Grades ':''}, regex = True)
    grades = {'12-Aug': '8-12', '12-Jul': '7-12',
            '12-Jun': '6-12', '6-Jan': '1-6',
            '8-Apr': '4-8', '8-Jan': '1-8', 'EC-12': '0-12',
            'EC-4': '0-4', 'EC-6': '0-6', 'PK-12': '0-12',
            'PK-3': '0-3', 'PK-6': '0-6', 'PK-KG': '0-1'}
    certification['cert_grades'] = certification['cert_grades'].replace(grades)
    certification['cert_grade_low'],certification['cert_grade_high'] = certification['cert_grades'].str.split('-').str
    certification['cert_grade_low'] = pd.to_numeric(certification.cert_grade_low, errors = 'coerce')
    certification['cert_grade_high'] = pd.to_numeric(certification.cert_grade_high, errors = 'coerce')


    # Only keep unexpired credentials
    certification['expiration'] = certification['expiration'].str[0:9]
    certification['expiration']= pd.to_datetime(certification['expiration'], errors = 'coerce') 
    certification = certification[certification.role == 'Teacher']
    timestamps = {'yr1213': '2012-07-01', 'yr1314': '2013-07-01', 'yr1415': '2014-07-01', 'yr1516': '2015-07-01',
                'yr1617': '2016-07-01', 'yr1718': '2017-07-01', 'yr1819': '2017-0701'}
    certification['expired'] = np.where(certification.expiration < pd.Timestamp(timestamps[year]), True, False)
    certification = certification[certification.expired == False]

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
    certification['certified'] = certification['cert_type'].map(cert_types)
    certification['vocational'] = np.where((certification['cert_type'] == "Vocational"), True, False)

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
    certification['certified_report'] = certification['cert_type'].map(cert_types_tea_report)

    # Generate binary grades certified variables. True if certified for any grades
    area = {'General Elementary (Self-Contained)': 'elem', 'Bilingual Education': 'biling', 'English Language Arts': 'ela',
        'Special Education': 'sped', 'Health and Physical Education': 'pe', 'Social Studies': 'ss','Mathematics': 'math',
        'Science': 'science', 'Vocational Education': 'voc', 'Fine Arts': 'art', 'Foreign Language': 'for',
        'Computer Science': 'cs', 'Other': 'other' }

    certification['cert_area'] = certification['cert_area'].map(area)

    # Elementary
    certification['cert_area_elem'] = np.where(certification['cert_area'] == "elem",
                                            True, False)
    certification['cert_area_elem'] = np.where((certification['cert_area'] == "biling") & 
                                        ((certification['cert_level'] == "Elementary") | 
                                        (certification['cert_level'] == "All Level")), True, certification.cert_area_elem)
    certification['cert_area_elem'] = np.where((certification['cert_area'] == "sped") & 
                                        ((certification['cert_level'] == "Elementary") | 
                                        (certification['cert_level'] == "All Level")),
                                        True, certification.cert_area_elem)
    # ELA 
    certification['cert_area_ela'] = np.where(certification['cert_area'] == 'ela', True, False)
    # SPED
    certification['cert_area_sped'] = np.where(certification['cert_area'] == 'sped', True, False)
    # PE
    certification['cert_area_pe'] = np.where(certification['cert_area'] == 'pe', True, False)
    # SS
    certification['cert_area_ss'] = np.where(certification['cert_area'] == 'ss', True, False)
    # Math
    certification['cert_area_math'] = np.where(certification['cert_area'] == 'math', True, False)
    certification['cert_area_high_math'] = np.where(certification.cert_grade_high > 8,
                                            certification.cert_area_math, False)
    # Science
    certification['cert_area_science'] = np.where(certification['cert_area'] == "science", True, False)
    certification['cert_area_high_science'] = np.where(certification.cert_grade_high > 8,
                                            certification.cert_area_science, False)
    # Voc
    certification['cert_area_voc'] = np.where(certification['cert_area'] == 'voc', True, False)
    # Fine arts
    certification['cert_area_art'] = np.where(certification['cert_area'] == 'art', True, False)
    # Foreign Language
    certification['cert_area_for'] = np.where(certification['cert_area'] == 'for', True, False)
    # CS
    certification['cert_area_cs'] = np.where(certification['cert_area'] == 'cs', True, False)

    certification = certification[certification.district != 'San Antonio']  # three teachers don't link to district number

    ###
    # Create any certification dataframe
    ###
    cert_yesno = certification[['teacher_id', 'certified', 'cert_area_elem', 
    'cert_area_ela', 'cert_area_sped', 'cert_area_pe', 'cert_area_ss', 
    'cert_area_math', 'cert_area_science', 'cert_area_voc', 'cert_area_for',
     'cert_area_cs']]
    teacher_yesno = cert_yesno.groupby(['teacher_id']).max()

    
    # Save to CSV
    filename = 'certs_' + year + '.csv'
    certification.to_csv(os.path.join(start.data_path, 'tea', 'teachers', filename))
