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

    if year == 'yr1112':
        filename = 'cref.dat'
    if year == 'yr1213':
        filename = 'CREF.txt'
    if year >= 'yr1314':
        filename = 'CREF.dat'
    cref = pd.read_csv(os.path.join(data_path, 'tea', 'cref', year, filename), sep=",")
    # Note: no district number in early files
    cref_tokeep = {'DISTNAME': 'distname',
                   'CAMPUS': 'campus',
                   'CAMPNAME': 'campname',
                   'CFLCHART': 'campischarter',
                   'CNTYNAME':  'cntyname_c',
                   'GRDTYPE': 'grade_range',
                   'REGION': 'region'}
    if year > 'yr1112':
        cref_tokeep['C_RATING'] = 'rating_academic_c'
    cref = filter_and_rename_cols(cref, cref_tokeep)
    return cref


def clean_cdem(year):
    """
    Reads demographic data from TAPR reports: from
    https://rptsvr1.tea.texas.gov/perfreport/tapr/2017/download/DownloadData.html 2011-12 from AEIS reports
    https://rptsvr1.tea.texas.gov/perfreport/aeis/2012/index.html :param year: year of demographic data to read
    :return: data frame with variables from cdem to keep
    """

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
        cdem_tokeep['CPETALLC'] = 'students_num'
    if year == 'yr1314':
        cdem_tokeep['CPETALLC'] = 'students_num'
    if year >= 'yr1415':
        cdem_tokeep['CPETALLC'] = 'students_num'
        cdem_tokeep['CPSTNOFC'] = 'teachers_nodegree_num'
        cdem_tokeep['CPSTBAFC'] = 'teachers_badegree_num'
        cdem_tokeep['CPSTMSFC'] = 'teachers_msdegree_num'
        cdem_tokeep['CPSTPHFC'] = 'teachers_phddegree_num'
    # filter and rename
    cdem = filter_and_rename_cols(cdem, cdem_tokeep)
    cdem['campus'] = cdem['campus'].apply(pd.to_numeric, errors='coerce')
    cdem['teachers_num'] = cdem['teachers_num'].apply(pd.to_numeric, errors='coerce')

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

    # English scores across two files in first years
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

    # Import dataa
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
        cscores_tokeep = {'CAMPUS': 'campus',
                          'a1_all_rs': 'alg_avescore',
                          'a1_all_d': 'alg_numtakers'}
    if subject == 'Biology':
        cscores_tokeep = {'CAMPUS': 'campus',
                          'bi_all_rs': 'bio_avescore',
                          'bi_all_d': 'bio_numtakers'}

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
    cscores['campus'] = cscores['campus'].apply(pd.to_numeric, errors='coerce')
    if year == 'yr1112':
        cscores['campus'] = cscores['campus'].apply(int)
    cscores = cscores.set_index('campus')
    print("There are ", len(cscores), "schools in ", subject, "dataset.")
    return cscores

def fix_duplicate_distname(df, distname_col = 'DISTNAME', cntyname_col = 'CNTYNAME'):
    dist_dict = [{'distname': 'BIG SANDY ISD', 'cntyname': 'UPSHUR', 'newname': 'BIG SANDY ISD (230901)'},
                 {'distname': 'BIG SANDY ISD', 'cntyname': 'POLK', 'newname': 'BIG SANDY ISD (187901)'},
                 {'distname': 'CENTERVILLE ISD', 'cntyname': 'LEON', 'newname': 'CENTERVILLE ISD (145902)'},
                 {'distname': 'CENTERVILLE ISD', 'cntyname': 'TRINITY', 'newname': 'CENTERVILLE ISD (228904)'},
                 {'distname': 'CHAPEL HILL ISD', 'cntyname': 'TITUS', 'newname': 'CHAPEL HILL ISD (225906)'},
                 {'distname': 'CHAPEL HILL ISD', 'cntyname': 'SMITH', 'newname': 'CHAPEL HILL ISD (212909)'},
                 {'distname': 'DAWSON ISD', 'cntyname': 'NAVARRO', 'newname': 'DAWSON ISD (175904)'},
                 {'distname': 'DAWSON ISD', 'cntyname': 'DAWSON', 'newname': 'DAWSON ISD (58902)'},
                 {'distname': 'EDGEWOOD ISD', 'cntyname': 'BEXAR', 'newname': 'EDGEWOOD ISD (15905)'},
                 {'distname': 'EDGEWOOD ISD', 'cntyname': 'VAN ZANDT', 'newname': 'EDGEWOOD ISD (234903)'},
                 {'distname': 'HIGHLAND PARK ISD', 'cntyname': 'DALLAS', 'newname': 'HIGHLAND PARK ISD (57911)'},
                 {'distname': 'HIGHLAND PARK ISD', 'cntyname': 'POTTER', 'newname': 'HIGHLAND PARK ISD (188903)'},
                 {'distname': 'HUBBARD ISD', 'cntyname': 'BOWIE', 'newname': 'HUBBARD ISD (19913)'},
                 {'distname': 'HUBBARD ISD', 'cntyname': 'HILL', 'newname': 'HUBBARD ISD (109905)'},
                 {'distname': 'MIDWAY ISD', 'cntyname': 'MCLENNAN', 'newname': 'MIDWAY ISD (161903)'},
                 {'distname': 'MIDWAY ISD', 'cntyname': 'CLAY', 'newname': 'MIDWAY ISD (39905)'},
                 {'distname': 'NORTHSIDE ISD', 'cntyname': 'BEXAR', 'newname': 'NORTHSIDE ISD (15915)'},
                 {'distname': 'NORTHSIDE ISD', 'cntyname': 'WILBARGER', 'newname': 'NORTHSIDE ISD (244905)'},
                 {'distname': 'VALLEY VIEW ISD', 'cntyname': 'HIDALGO', 'newname': 'VALLEY VIEW ISD (108916)'},
                 {'distname': 'VALLEY VIEW ISD', 'cntyname': 'COOKE', 'newname': 'VALLEY VIEW ISD (49903)'},
                 {'distname': 'WYLIE ISD', 'cntyname': 'COLLIN', 'newname': 'WYLIE ISD (43914)'},
                 {'distname': 'WYLIE ISD', 'cntyname': 'TAYLOR', 'newname': 'WYLIE ISD (221912)'},
                 {'distname': 'RICHARD MILBURN ALTER HIGH SCHOOL', 'cntyname': 'BELL',
                  'newname': 'RICHARD MILBURN ALTER HIGH SCHOOL (14801)'},
                 {'distname': 'RICHARD MILBURN ALTER HIGH SCHOOL', 'cntyname': 'NUECES',
                  'newname': 'RICHARD MILBURN ALTER HIGH SCHOOL (178804)'}
                 ]
    for entry in dist_dict:
        df.loc[(df[distname_col] == entry['distname']) & (df[cntyname_col] == entry['cntyname']), distname_col] = entry[
            'newname']
    return df


def clean_cdays(year):
    """
    Reads number of schools days from dataset from PIR
    :param year:
    :return: renamed and filtered variables, with min, mean, and max by district
    Note: only available for yr1617 and 1718
    """
    filename = 'days_' + year + '.csv'
    cdays = pd.read_csv(os.path.join(data_path, 'tea', 'cdays', filename), sep=",")
    cdays_to_keep = {'DISTRICT': 'district', 'DISTNAME': 'distname',
                    'CAMPUS': 'campus', 'CAMPNAME': 'campname',
                    'TRACK': 'track',
                    'TOTAL_DAYS': 'days'}
    cdays = filter_and_rename_cols(cdays, cdays_to_keep)
    cdays = cdays.groupby(by=['district', 'distname', 'campus', 'campname']).max().reset_index()
    cdays = cdays[['district', 'distname', 'campus', 'campname', 'days']]

    return cdays