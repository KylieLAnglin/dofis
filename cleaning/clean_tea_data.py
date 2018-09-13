import pandas as pd
import cleaning
import os
import start
import csv

# # Start by making 2016-17 dataset, then generalize to all years

# # Basic Descriptives - DREF
# data from: https://tea.texas.gov/perfreport/tapr/index.html
# reference of labels: https://rptsvr1.tea.texas.gov/perfreport/tapr/2016/download/dstaff.html


years =  ['yr1213', 'yr1314', 'yr1415', 'yr1516', 'yr1617']
for year in years:
    print(year)
    if year == 'yr1213':
        filename = 'DREF.txt'
    else:
        filename = 'DREF.dat'
    dref = pd.read_csv(os.path.join(start.data_path, 'dref', year, filename), sep=",")
    dref_tokeep = {'DISTRICT': 'district',
                   'DISTNAME': 'distname',
                   'DFLCHART': 'distischarter',
                   'D_RATING': 'rating',
                   'CNTYNAME': 'cntyname'
                   }
    dref = cleaning.filter_and_rename_cols(dref, dref_tokeep)

    # # Demographic data - DDEM
    # data from: https://tea.texas.gov/perfreport/tapr/index.html
    # reference of labels: https://rptsvr1.tea.texas.gov/perfreport/tapr/2016/download/dstaff.html
    if year == 'yr1213':
        filename = 'DISTPROF.txt'
    else:
        filename = 'DISTPROF.dat'
    ddem = pd.read_csv(os.path.join(start.data_path, 'ddem', year, filename), sep=",")
    ddem_tokeep = {
        'DISTRICT': 'district',
        'DPSATOFC': 'teachers_num',
        'DPST00FC': 'teachers_new_num',
        'DPSTEXPA': 'teachers_exp_ave',
        'DPSTTENA': 'teachers_tenure_ave',
        'DPSTURND': 'teachers_turnover_denom',
        'DPSTURNN': 'teacher_turnover_num',
        'DPSTURNR': 'teachers_turnover_ratio',
        'DPSTNOFC': 'teachers_nodegree_num',
        'DPSTBAFC': 'teachers_badegree_num',
        'DPSTMSFC': 'teachers_msdegree_num',
        'DPSTPHFC': 'teachers_phddegree_num',
        'DPETALLC': 'students_num',
        'DPETECOC': 'students_frpl_num',
        'DPETHISC': 'students_hisp_num',
        'DPETWHIC': 'students_white_num',
        'DPETBLAC': 'students_black_num'}
    ddem = cleaning.filter_and_rename_cols(ddem, ddem_tokeep)

    # # Scores - dscores
    # data from: https://tea.texas.gov/student.assessment/staar/aggregate/
    # labels from: https://tea.texas.gov/student.assessment/staar/variables/

    if year == 'yr1213':
        filename = 'dfy13e3.dat'
    if year == 'yr1314':
        filename = 'dfy14e3.dat'
    if year == 'yr1415':
        filename = 'dfy15e3.dat'
    if year == 'yr1516':
        filename = 'dfy16e3.dat'
    if year == 'yr1617':
        filename = 'dfy17e3.dat'
    if year == 'yr1718':
        filename = 'dfy18e3.dat'
    dscores_3rd = pd.read_csv(os.path.join(start.data_path, 'dscores', '3rd', filename), sep=",")
    subject = '3rd'
    dscores_tokeep = {'DISTRICT': 'district',
                      "r_all_rs": "r_" + subject + "_avescore",
                      "r_all_d": "r_" + subject + "_numtakers",
                      "m_all_d": "m_" + subject + "_avescore",
                      "m_all_rs": "m_" + subject + "_numtakers"}
    dscores_3rd = cleaning.filter_and_rename_cols(dscores_3rd, dscores_tokeep)

    grade_list = ['4th', '5th', '6th', '7th', '8th']
    if year == 'yr1213':
        filenames = ['dfy12e4.dat', 'dfy12e5.dat', 'dfy12e6.dat', 'dfy12e7.dat', 'dfy12e8.dat']
    if year == 'yr1213':
        filenames = ['dfy13e4.dat', 'dfy13e5.dat', 'dfy13e6.dat', 'dfy13e7.dat', 'dfy13e8.dat']
    if year == 'yr1314':
        filenames = ['dfy14e4.dat', 'dfy14e5.dat', 'dfy14e6.dat', 'dfy14e7.dat', 'dfy14e8.dat']
    if year == 'yr1415':
        filenames = ['dfy15e4.dat', 'dfy15e5.dat', 'dfy15e6.dat', 'dfy15e7.dat', 'dfy15e8.dat']
    if year == 'yr1516':
        filenames = ['dfy16e4.dat', 'dfy16e5.dat', 'dfy16e6.dat', 'dfy16e7.dat', 'dfy16e8.dat']
    if year == 'yr1617':
        filenames = ['dfy17e4.dat', 'dfy17e5.dat', 'dfy17e6.dat', 'dfy17e7.dat', 'dfy17e8.dat']
    if year == 'yr1718':
        filenames = ['dfy18e4.dat', 'dfy18e5.dat', 'dfy18e6.dat', 'dfy18e7.dat', 'dfy18e8.dat']
    for file, grade in zip(filenames, grade_list):
        dscores_grade = pd.read_csv(os.path.join(start.data_path, 'dscores', grade, file), sep=",")
        dscores_tokeep = {'DISTRICT': 'district',
                          "r_all_rs": "r_" + grade + "_avescore",
                          "r_all_d": "r_" + grade + "_numtakers",
                          "m_all_d": "m_" + grade + "_avescore",
                          "m_all_rs": "m_" + grade + "_numtakers"}
        dscores_grade = cleaning.filter_and_rename_cols(dscores_grade, dscores_tokeep)
        dscores = dscores_3rd.merge(dscores_grade)

    subject_list = ['Algebra', 'Biology', 'EnglishI', 'EnglishII', 'USHistory']
    if year == 'yr1112':
        filenames = ['dfy12ea1.dat', 'dfy12ebi.dat', 'dfy12er1.dat', 'dfy12er2.dat', 'dfy12eus.dat']
    if year == 'yr1213':
        filenames = ['dfy13ea1.dat', 'dfy13ebi.dat', 'dfy13er1.dat', 'dfy13er2.dat', 'dfy13eus.dat']
    if year == 'yr1314':
        filenames = ['dfy14ea1.dat', 'dfy14ebi.dat', 'dfy14ee1.dat', 'dfy14ee2.dat', 'dfy14eus.dat']
    if year == 'yr1415':
        filenames = ['dfy15ea1.dat', 'dfy15ebi.dat', 'dfy15ee1.dat', 'dfy15ee2.dat', 'dfy15eus.dat']
    if year == 'yr1516':
        filenames = ['dfy16ea1.dat', 'dfy16ebi.dat', 'dfy16ee1.dat', 'dfy16ee2.dat', 'dfy16eus.dat']
    if year == 'yr1617':
        filenames = ['dfy17ea1.dat', 'dfy17ebi.dat', 'dfy17ee1.dat', 'dfy17ee2.dat', 'dfy17eus.dat']
    if year == 'yr1718':
        filenames = ['dfy18ea1.dat', 'dfy18ebi.dat', 'dfy18ee1.dat', 'dfy18ee2.dat', 'dfy18eus.dat']
    for subject, file in zip(subject_list, filenames):
        print(subject)
        try:
            dscores_subject = pd.read_csv(os.path.join(start.data_path, 'dscores', subject, file), sep=",")
        except:
            new_path = cleaning.fix_parser_error(os.path.join(start.data_path, 'dscores', subject, file))
            dscores_subject = pd.read_csv(new_path, sep=",")

        if subject == 'Algebra':
            dscores_tokeep = {"DISTRICT": "district",
                              "a1_all_rs": "alg_avescore",
                              "a1_all_d": "alg_numtakers"}
        if subject == 'Biology':
            dscores_tokeep = {"DISTRICT": "district",
                              "bi_all_rs": "bio_avescore",
                              "bi_all_d": "bio_numtakers"}
        if subject == 'EnglishI':
            if year == 'yr1112' or year == 'yr1213':
                dscores_tokeep = {"DISTRICT": "district",
                                  "r1_all_rs": "eng1_avescore",
                                  "r1_all_d": "eng1_numtakers"}
            else:
                dscores_tokeep = {"DISTRICT": "district",
                                  "e1_all_rs": "eng1_avescore",
                                  "e1_all_d": "eng1_numtakers"}
        if subject == 'EnglishII':
            if year == 'yr1112' or year == 'yr1213':
                dscores_tokeep = {"DISTRICT": "district",
                                  "r2_all_rs": "eng2_avescore",
                                  "r2_all_d": "eng2_numtakers"}
            else:
                dscores_tokeep = {"DISTRICT": "district",
                                  "e2_all_rs": "eng2_avescore",
                                  "e2_all_d": "eng2_numtakers"}
        if subject == 'USHistory':
            dscores_tokeep = {"DISTRICT": "district",
                              "us_all_rs": "us_avescore",
                              "us_all_d": "us_numtakers"}
        dscores_subject = cleaning.filter_and_rename_cols(dscores_subject, dscores_tokeep)
        dscores = dscores.merge(dscores_subject, on = ['district'])

    dscores['year'] = year
    yr_file = 'descriptives_' + year + '.csv'

    dscores.to_csv((os.path.join(start.data_path, yr_file )))