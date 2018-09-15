import pandas as pd
import os
import shutil
from .start import data_path

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
    temp_directory = os.path.join(data_path, 'tea', 'temp')
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
    if year == 'yr1112':
        filename = 'DREF.csv'
    elif year == 'yr1213':
        filename = 'DREF.txt'
    elif year == 'yr1718':
        year = 'yr1617' #delete when reference data updated
        filename = 'DREF.dat'
    else:
        filename = 'DREF.dat'
    dref = pd.read_csv(os.path.join(data_path, 'tea', 'dref',  year, filename), sep=",")

    if year == 'yr1112':
        dref_tokeep = {'DISTRICT': 'district',
                       'DISTNAME': 'distname',
                       'DFLCHART': 'distischarter',
                       'CNTYNAME': 'cntyname'
                       }
    else:
        dref_tokeep = {'DISTRICT': 'district',
                       'DISTNAME': 'distname',
                       'DFLCHART': 'distischarter',
                       'D_RATING': 'rating',
                       'CNTYNAME': 'cntyname'
                       }
    dref = filter_and_rename_cols(dref, dref_tokeep)
    if year == 'yr1112':
        dref['district'] = dref['district'].str.strip('\'')
        dref['district'] = dref['district'].apply(int)
    print("There are ", len(dref), 'districts in dref')
    return dref

def clean_ddem(year):
    if year == 'yr1213':
        filename = 'DISTPROF.txt'
    else:
        filename = 'DISTPROF.dat'
    if year == 'yr1718':
        year = 'yr1617'
    if year == 'yr1112':
        ddem1 = pd.read_csv(os.path.join(data_path, 'tea', 'ddem', year, 'dstud.csv'), sep=",")
        ddem2 = pd.read_csv(os.path.join(data_path, 'tea', 'ddem', year, 'dstaf.csv'), sep=",")
        ddem = ddem1.merge(ddem2, on= 'DISTRICT', how = 'outer')
        ddem['DISTRICT'] = ddem['DISTRICT'].str.strip('\'')
        ddem['DISTRICT'] = ddem['DISTRICT'].apply(int)
        ddem_tokeep = {
            'DISTRICT': 'district',
            'DPSATOFC': 'teachers_num',
            'DPST00FC': 'teachers_new_num',
            'DPSTEXPA': 'teachers_exp_ave',
            'DPSTTENA': 'teachers_tenure_ave',
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
    else:
        ddem = pd.read_csv(os.path.join(data_path, 'tea', 'ddem', year, filename), sep=",")
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
        dscores = pd.read_csv(os.path.join(data_path, 'tea', 'dscores', subject, file), sep=",")
    except:
        new_path = fix_parser_error(os.path.join(data_path, 'tea', 'dscores', subject, file))
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

    dscores = filter_and_rename_cols(dscores, dscores_tokeep)
    if year == 'yr1112':
        dscores['district'] = dscores['district'].apply(int)
    dscores = dscores.set_index('district')
    print("There are ", len(dscores), "districts in ", "dataset.")
    #num_dups = len(dscores[dscores.index.duplicated(keep = False) == True])
    #print('There are', num_dups, ' duplicate indices.')

    return dscores


