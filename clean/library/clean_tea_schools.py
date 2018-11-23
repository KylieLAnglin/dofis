import os
import pandas as pd
import shutil

try:
    from .start import data_path
except ModuleNotFoundError:
    data_path = '/Users/kylieleblancKylie/domino/dofis/data/'


def filter_and_rename_cols(df, mydict):
    """
    Keep some original cols from a dataframe, rename them to new column names
    Return a new data frame

    Arguments:
    df = data frame
    dict keys = original column names you want to keep
    dict values = new column names
    """
    df = df[list(mydict.keys())]
    new_df = df.rename(index=str, columns=mydict)
    return new_df

def fix_parser_error(input_path):
    """
    Some older datasets have observation data across two rows
    :param input_path: Location of data set
    :return: data set where columns are all in one row
    """
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
    return (temp_path)


def clean_cref(year):
    """
    Reads reference data from TABR reports https://rptsvr1.tea.texas.gov/perfreport/tapr/2017/download/DownloadData.html
    :param year:
    :return:
    """
    if year == 'yr1718':
        year = 'yr1617'
    if year == 'yr1112':
        filename = 'cref.dat'
    if year == 'yr1213':
        filename = 'CREF.txt'
    if year >= 'yr1314':
        filename = 'CREF.dat'
    cref = pd.read_csv(os.path.join(data_path, 'tea', 'cref', year, filename), sep=",")
    cref_tokeep = {'DISTNAME': 'distname',
                   'DISTRICT': 'district',
                   'CAMPUS': 'campus',
                   'CAMPNAME': 'campname',
                   'CFLCHART': 'campischarter',
                   'GRDTYPE': 'grade_range',
                   'REGION': 'region'}
    if year > 'yr1112':
        cref_tokeep['C_RATING'] = 'rating_c'
    cref = filter_and_rename_cols(cref, cref_tokeep)
    return cref


def clean_cdem(year):
    """
    Reads demographic data from TAPR reports: from
    https://rptsvr1.tea.texas.gov/perfreport/tapr/2017/download/DownloadData.html 2011-12 from AEIS reports
    https://rptsvr1.tea.texas.gov/perfreport/aeis/2012/index.html :param year: year of demographic data to read
    :return: data frame with variables from cdem to keep TODO: Can add classize later
    """
    if year == 'yr1718':
        year = 'yr1617'
    if year == 'yr1213':
        filename = 'CAMPPROF.txt'
    else:
        filename = 'CAMPPROF.dat'
    cdem_tokeep = {
        'CAMPUS': 'campus',
        'CPSTTOFC': 'teachers_num',
        'CPST00FC': 'teachers_new_num',
        'CPSTEXPA': 'teachers_exp_ave',
        'CPSTTENA': 'teachers_tenure_ave',
        'CPETECOC': 'students_frpl_num',
        'CPETHISC': 'students_hisp_num',
        'CPETWHIC': 'students_white_num',
        'CPETBLAC': 'students_black_num',
        'CPETINDC': 'students_amind_num',
        'CPETASIC': 'students_asian_num',
        'CPETPCIC': 'students_paci_num',
        'CPETTWOC': 'students_tworaces_num'
    }
    # import data
    if year == 'yr1112':
        cdem1 = pd.read_csv(os.path.join(data_path, 'tea', 'cdem', year, 'cstud.dat'), sep=",")
        cdem2 = pd.read_csv(os.path.join(data_path, 'tea', 'cdem', year, 'cstaf.dat'), sep=",")
        cdem = cdem1.merge(cdem2, on='CAMPUS', how='outer')
        cdem['CAMPUS'] = cdem['CAMPUS'].apply(int)
    else:
        cdem = pd.read_csv(os.path.join(data_path, 'tea', 'cdem', year, filename), sep=",")
    # address variable name changes across years
    if year == 'yr1112':
        cdem_tokeep['CPETALLC'] = 'students_num'
    if year == 'yr1213':
        cdem_tokeep['CA0GR12N'] = 'students_num'
    if year == 'yr1314':
        cdem_tokeep['CA0GR13N'] = 'students_num'
    if year >= 'yr1415':
        cdem_tokeep['CPETALLC'] = 'students_num'
        cdem_tokeep['CPSTNOFC'] = 'teachers_nodegree_num'
        cdem_tokeep['CPSTBAFC'] = 'teachers_badegree_num'
        cdem_tokeep['CPSTMSFC'] = 'teachers_msdegree_num'
        cdem_tokeep['CPSTPHFC'] = 'teachers_phddegree_num'
    # filter and rename
    cdem = filter_and_rename_cols(cdem, cdem_tokeep)
    print("There are ", len(cdem), 'schools in cdem', year)
    return cdem


def clean_cscores(year, subject):
    """
    Reads STAAR scores from
    https://tea.texas.gov/student.assessment/staar/aggregate/
    :param year: year to read
    :param subject: subject to read (see subject_dict keys for subjects
    :return:
    """
    # File name
    file_yr = year[4:6]
    subject_dict = {'3rd': 'e3', '4th': 'e4', '5th': 'e5', '6th': 'e6', '7th': 'e7', '8th': 'e8',
                    'Algebra': 'ea1', 'Biology': 'ebi', 'EnglishI': 'ee1', 'EnglishII': 'ee2', 'USHistory': 'eus'}
    file_sub = subject_dict[subject]
    file = 'cfy' + file_yr + file_sub + '.dat'

    if year in ['yr1112', 'yr1213'] and subject in ['EnglishI', 'EnglishII']:
        subject_dict = {'EnglishI': 'ew1', 'EnglishII': 'ew2'}
        file = 'cfy' + file_yr + subject_dict[subject] + '.dat'
        # need two files for early English scores (reading and writing) TODO: combine reading and writing
        try:
            cscores2 = pd.read_csv(os.path.join(data_path, 'tea', 'cscores', year, file), sep=",")
        except:
            new_path = fix_parser_error(os.path.join(data_path, 'tea', 'cscores', year, file))
            cscores2 = pd.read_csv(new_path, sep=",")
        subject_dict = {'EnglishI': 'er1', 'EnglishII': 'er2'}
        file = 'cfy' + file_yr + subject_dict[subject] + '.dat'
    try:
        cscores = pd.read_csv(os.path.join(data_path, 'tea', 'cscores', year, file), sep=",")
    except:
        new_path = fix_parser_error(os.path.join(data_path, 'tea', 'cscores', year, file))
        cscores = pd.read_csv(new_path, sep=",")
    if subject not in ['3rd', '4th', '5th', '6th', '7th', '8th', 'Algebra', 'Biology', 'EnglishI', 'EnglishII',
                       'USHistory']:
        return 'invalid subject'
    if subject in ['3rd', '4th', '5th', '6th', '7th', '8th']:
        cscores_tokeep = {'CAMPUS': 'campus',
                          "r_all_rs": "r_" + subject + "_avescore",
                          "r_all_d": "r_" + subject + "_numtakers",
                          "m_all_rs": "m_" + subject + "_avescore",
                          "m_all_d": "m_" + subject + "_numtakers"}
    if subject == 'Algebra':
        cscores_tokeep = {"CAMPUS": "campus",
                          "a1_all_rs": "alg_avescore",
                          "a1_all_d": "alg_numtakers"}
    if subject == 'Biology':
        cscores_tokeep = {'CAMPUS': 'campus',
                          "bi_all_rs": "bio_avescore",
                          "bi_all_d": "bio_numtakers"}

    if subject == 'EnglishI':
        if year == 'yr1112' or year == 'yr1213':
            cscores['e1_all_rs'] = cscores['r1_all_rs'] + cscores2['w1_all_rs']
            cscores['e1_all_d'] = cscores['r1_all_d']
        cscores_tokeep = {"CAMPUS": "campus",
                          "e1_all_rs": "eng1_avescore",
                          "e1_all_d": "eng1_numtakers"}

    if subject == 'EnglishII':
        if year == 'yr1112' or year == 'yr1213':
            cscores['e2_all_rs'] = cscores['r2_all_rs'] + cscores2['w2_all_rs']
            cscores['e2_all_d'] = cscores['r2_all_d']

        cscores_tokeep = {"CAMPUS": "campus",
                          "e2_all_rs": "eng2_avescore",
                          "e2_all_d": "eng2_numtakers"}
    if subject == 'USHistory':
        cscores_tokeep = {"CAMPUS": "campus",
                          "us_all_rs": "us_avescore",
                          "us_all_d": "us_numtakers"}

    cscores = filter_and_rename_cols(cscores, cscores_tokeep)
    if year == 'yr1112':
        cscores['campus'] = cscores['campus'].apply(int)
    cscores = cscores.set_index('campus')
    print("There are ", len(cscores), "districts in ", subject, "dataset.")
    # num_dups = len(dscores[dscores.index.duplicated(keep = False) == True])
    # print('There are', num_dups, ' duplicate indices.')
    return cscores
