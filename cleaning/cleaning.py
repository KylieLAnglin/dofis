import pandas as pd
import os
import shutil
import start


def filter_and_rename_cols(df, dict):
    """
    Keep some original cols from a dataframe, rename them to new column names
    Return a new data frame

    Arguments:
    df = data frame
    dict keys = original column names you want to keep
    dict values = new column names
    """
    df = df[list(dict.keys())]
    new_df = df.rename(index=str, columns=dict)
    return new_df

def fix_parser_error(input_path):
    temp_directory = os.path.join(start.data_path, 'temp')
    temp_file = os.path.basename(input_path)
    temp_path = os.path.join(temp_directory, temp_file)

    print('Got a parser error - concatenating first two lines of text file to remedy!')
    shutil.copy(input_path, temp_path)

    with open(temp_path, 'r') as file:
        text_contents = file.read()
    text_contents = text_contents.replace('\n', '', 1)
    with open(temp_path, 'w') \
            as file:
        file.write(text_contents)
    return(temp_path)


def clean_dref(year):
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
    dref = filter_and_rename_cols(dref, dref_tokeep)
    print("There are ", len(dref), 'districts in dref')
    return dref

def clean_ddem(year):
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
    ddem = filter_and_rename_cols(ddem, ddem_tokeep)
    print("There are ", len(ddem), 'districts in ddem')
    return ddem


def clean_scores(year, subject):
    file_yr = year[4:6]
    subject_dict= {'3rd': 'e3', '4th': 'e4', '5th': 'e5', '6th': 'e6', '7th': 'e7', '8th': 'e8',
                   'Algebra': 'ea1', 'Biology': 'ebi', 'EnglishI': 'ee1', 'EnglishII': 'ee2', 'USHistory': 'eus'}
    file_sub = subject_dict[subject]
    file = 'dfy' + file_yr + file_sub + '.dat'

    if year in ['yr1112', 'yr1213'] and subject in ['EnglishI', 'EnglishII']:
        subject_dict= {'EnglishI': 'er1', 'EnglishII': 'er2'}
        file = 'dfy' + file_yr + subject_dict[subject] + '.dat'

    try:
        dscores = pd.read_csv(os.path.join(start.data_path, 'dscores', subject, file), sep=",")
    except:
        new_path = fix_parser_error(os.path.join(start.data_path, 'dscores', subject, file))
        dscores = pd.read_csv(new_path, sep=",")

    if subject not in ['3rd', '4th', '5th', '6th', '7th', '8th', 'Algebra', 'Biology', 'EnglishI', 'EnglishII', 'USHistory']:
        return 'invalid subject'
    if subject in ['3rd', '4th', '5th', '6th', '7th', '8th']:
        dscores_tokeep = {'DISTRICT': 'district',
                          "r_all_rs": "r_" + subject + "_avescore",
                          "r_all_d": "r_" + subject + "_numtakers",
                          "m_all_d": "m_" + subject + "_avescore",
                          "m_all_rs": "m_" + subject + "_numtakers"}
    if subject == 'Algebra':
        dscores_tokeep = {"DISTRICT": "district",
                          "DNAME": 'distname',
                          "a1_all_rs": "alg_avescore",
                          "a1_all_d": "alg_numtakers"}
    if subject == 'Biology':
        dscores_tokeep = {"DISTRICT": "district",
                          "DNAME": 'distname',
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
                          "DNAME": 'distname',
                          "us_all_rs": "us_avescore",
                          "us_all_d": "us_numtakers"}

    dscores = filter_and_rename_cols(dscores, dscores_tokeep)
    dscores = dscores.set_index('district')
    print("There are ", len(dscores), "districts in ", "dataset.")
    num_dups = len(dscores[dscores.index.duplicated(keep = False)])
    print('There are', num_dups, ' duplicate indices.')

    return dscores

