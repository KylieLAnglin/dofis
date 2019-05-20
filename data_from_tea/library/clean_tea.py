import os
import pandas as pd
import numpy as np
import shutil
from .start import data_path
from library import clean_tea_schools


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


def clean_dref(year):
    """
    Reads district reference data from:
    https://rptsvr1.tea.texas.gov/perfreport/tapr/2017/download/DownloadData.html
    Manually add financial ratings from:
    https://tealprod.tea.state.tx.us/First/forms/Main.aspx

    :param year: year of data set to read
    :return: data frame with variables from dref to keep
    """
    if year == 'yr1112':
        filename = 'DREF.csv'
    elif year == 'yr1213':
        filename = 'DREF.txt'
    else:
        filename = 'DREF.dat'
    dref = pd.read_csv(os.path.join(data_path, 'tea', 'dref', year, filename), sep=",")
    dref_tokeep = {'DISTRICT': 'district',
                   'DISTNAME': 'distname',
                   'DFLCHART': 'distischarter',
                   'CNTYNAME': 'cntyname'
                   }
    if year > 'yr1112':
        dref_tokeep['D_RATING'] = 'rating_academic'
    dref = filter_and_rename_cols(dref, dref_tokeep)
    if year == 'yr1112':
        dref['district'] = dref['district'].str.strip('\'')
        dref['district'] = dref['district'].apply(int)

    # Add financial rating (based on year before - https://tealprod.tea.state.tx.us/First/forms/Main.aspx)
    if year in ['yr1112', 'yr1213', 'yr1314']:
        dref['rating_financial'] = None
    if year == 'yr1415':
        failed_districts = [9901, 59902, 115902, 123910, 222901, 242905, 108914, 14905, 131001, 84904, 137904, 237902]
        dref['rating_financial'] = np.where((dref['district'].isin(failed_districts)), "Fail", "Pass")
    if year == 'yr1516':
        failed_districts = [37908, 68901, 123910, 227907]
        dref['rating_financial'] = np.where((dref['district'].isin(failed_districts)), "Fail", "Pass")
    if year == 'yr1617':
        failed_districts = [92906, 163904, 174902, 70901, 7906]
        dref['rating_financial'] = np.where((dref['district'].isin(failed_districts)), "Fail", "Pass")
    if year == 'yr1718':
        failed_districts = [54901, 64903, 71903, 108902, 176902]
        dref['rating_financial'] = np.where((dref['district'].isin(failed_districts)), "Fail", "Pass")

    if year not in ['yr1112', 'yr1213', 'yr1314']:
        dref['eligible'] = np.where((dref['rating_academic'].isin(['M', 'A'])
                                     & (dref['rating_financial'] == 'Pass')
                                     & (dref['distischarter'] == 'N')), True,
                                    False)  # M= Meets standard, A = Meets alternative standard

    print("There are ", len(dref), 'districts in dref')
    return dref


def clean_cref_numschools(year):
    """
    Reads campus reference data from https://rptsvr1.tea.texas.gov/perfreport/tapr/2017/download/DownloadData.html
    :param year: df of district and number of schools
    :return:
    """

    if year == 'yr1112':
        filename = 'cref.dat'
    if year == 'yr1213':
        filename = 'CREF.txt'
    if year >= 'yr1314':
        filename = 'CREF.dat'
    cref = pd.read_csv(os.path.join(data_path, 'tea', 'cref', year, filename), sep=",")
    cref = pd.DataFrame(cref.groupby(['DISTNAME', 'CNTYNAME'])['CAMPUS'].count())
    cref_tokeep = {'DISTNAME': 'distname',
                   'CAMPUS': 'schools_num',
                   'CNTYNAME': 'cntyname'}
    cref = cref.reset_index()
    cref = filter_and_rename_cols(cref, cref_tokeep)

    return cref

# district type
# https://tea.texas.gov/acctres/analyze/years.html
def clean_dtype(year):
    files = {'yr1112': 'district1112.xls',
             'yr1213': 'district1213.xls',
             'yr1314': 'district1314.xls',
             'yr1415': 'district1415.xlsx',
             'yr1516': 'district1516.xlsx',
             'yr1617': 'district1617.xls',
             'yr1718': 'district1617.xls'}  # update when type updates
    sheets = {'yr1112': 'district1112',
              'yr1213': 'district1213',
              'yr1314': 'district1314',
              'yr1415': 'district1415',
              'yr1516': 'district1516',
              'yr1617': 'district1617',
              'yr1718': 'district1617'}  # update when type undates
    dtype_to_keep = {'District': 'district',
                     'Type': 'type',
                     'Description': 'type_description'}
    filename = files[year]
    xls = pd.ExcelFile(os.path.join(data_path, 'tea', 'dtype', filename))
    dtype = xls.parse(sheets[year], skiprows=2)
    dtype = filter_and_rename_cols(dtype, dtype_to_keep)
    print("There are ", len(dtype), 'districts in dref')
    return dtype


def clean_ddem(year):
    """
    Reads district level demographic data pulled from:
     https://rptsvr1.tea.texas.gov/perfreport/tapr/2017/download/DownloadData.html
    :param year: year of demographic data to read
    :return: data frame with variables from ddem to keep
    """

    if year == 'yr1213':
        filename = 'DISTPROF.txt'
    else:
        filename = 'DISTPROF.dat'
    ddem_tokeep = {
        'DISTRICT': 'district',
        'DPSTTOFC': 'teachers_num',
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
        'DPETBLAC': 'students_black_num',
        'DPETINDC': 'students_amind_num',
        'DPETASIC': 'students_asian_num',
        'DPETPCIC': 'students_paci_num',
        'DPETTWOC': 'students_tworaces_num'}
    if year == 'yr1112':
        ddem1 = pd.read_csv(os.path.join(data_path, 'tea', 'ddem', year, 'dstud.csv'), sep=",")
        ddem2 = pd.read_csv(os.path.join(data_path, 'tea', 'ddem', year, 'dstaf.csv'), sep=",")
        ddem = ddem1.merge(ddem2, on='DISTRICT', how='outer')
        ddem['DISTRICT'] = ddem['DISTRICT'].str.strip('\'')
        ddem['DISTRICT'] = ddem['DISTRICT'].apply(int)
    else:
        ddem = pd.read_csv(os.path.join(data_path, 'tea', 'ddem', year, filename), sep=",")
        ddem_tokeep['DPSTURND'] = 'teachers_turnover_denom'
        ddem_tokeep['DPSTURNN'] = 'teachers_turnover_num'
        ddem_tokeep['DPSTURNR'] = 'teachers_turnover_ratio'
    ddem = filter_and_rename_cols(ddem, ddem_tokeep)
    ddem['teachers_num'] = pd.to_numeric(ddem.teachers_num, errors='coerce')
    print("There are ", len(ddem), 'districts in ddem')
    return ddem



def clean_scores(year, subject):
    """
    Reads STAAR scores from
    https://tea.texas.gov/Student_Testing_and_Accountability/Testing/State_of_Texas_Assessments_of_Academic_Readiness_(STAAR)/STAAR_Aggregate_Data_for_2017-2018/
    :param year: year to read
    :param subject: subject to read (see subject_dict keys for subjects
    :return:
    """
    file_yr = year[4:6]
    subject_dict = {'3rd': 'e3', '4th': 'e4', '5th': 'e5', '6th': 'e6', '7th': 'e7', '8th': 'e8',
                    'Algebra': 'ea1', 'Biology': 'ebi', 'EnglishI': 'ee1', 'EnglishII': 'ee2', 'USHistory': 'eus'}
    file_sub = subject_dict[subject]
    file = 'dfy' + file_yr + file_sub + '.dat'

    if year in ['yr1112', 'yr1213'] and subject in ['EnglishI', 'EnglishII']:
        subject_dict = {'EnglishI': 'ew1', 'EnglishII': 'ew2'}
        file = 'dfy' + file_yr + subject_dict[subject] + '.dat'
        # need two files for early English scores (reading and writing)
        try:
            dscores2 = pd.read_csv(os.path.join(data_path, 'tea', 'dscores', subject, file), sep=",")
        except:
            new_path = fix_parser_error(os.path.join(data_path, 'tea', 'dscores', subject, file))
            dscores2 = pd.read_csv(new_path, sep=",")
        subject_dict = {'EnglishI': 'er1', 'EnglishII': 'er2'}
        file = 'dfy' + file_yr + subject_dict[subject] + '.dat'
    try:
        dscores = pd.read_csv(os.path.join(data_path, 'tea', 'dscores', subject, file), sep=",")
    except:
        new_path = fix_parser_error(os.path.join(data_path, 'tea', 'dscores', subject, file))
        dscores = pd.read_csv(new_path, sep=",")

    if subject not in ['3rd', '4th', '5th', '6th', '7th', '8th', 'Algebra', 'Biology', 'EnglishI', 'EnglishII',
                       'USHistory']:
        return 'invalid subject'
    if subject in ['3rd', '4th', '6th', '7th']:
        dscores_tokeep = {'DISTRICT': 'district',
                          "r_all_rs": "r_" + subject + "_avescore",
                          "r_all_d": "r_" + subject + "_numtakers",
                          "m_all_rs": "m_" + subject + "_avescore",
                          "m_all_d": "m_" + subject + "_numtakers"}
    if subject in ['5th', '8th']:
        dscores_tokeep = {'DISTRICT': 'district',
                          "r_all_rs": "r_" + subject + "_avescore",
                          "r_all_d": "r_" + subject + "_numtakers",
                          "m_all_rs": "m_" + subject + "_avescore",
                          "m_all_d": "m_" + subject + "_numtakers",
                          "s_all_rs": "s_" + subject + "_avescore",
                          "s_all_d": "s_" + subject + "_numtakers"}

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
            dscores['e1_all_rs'] = dscores['r1_all_rs'] + dscores2['w1_all_rs']
            dscores['e1_all_d'] = dscores['r1_all_d']
        dscores_tokeep = {"DISTRICT": "district",
                          "e1_all_rs": "eng1_avescore",
                          "e1_all_d": "eng1_numtakers"}

    if subject == 'EnglishII':
        if year == 'yr1112' or year == 'yr1213':
            dscores['e2_all_rs'] = dscores['r2_all_rs'] + dscores2['w2_all_rs']
            dscores['e2_all_d'] = dscores['r2_all_d']

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
    print("There are ", len(dscores), "districts in ", subject, "dataset.")
    # num_dups = len(dscores[dscores.index.duplicated(keep = False) == True])
    # print('There are', num_dups, ' duplicate indices.')

    return dscores

def clean_ddays(year):
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
    cdays = cdays.groupby(by=['district', 'distname', 'campus', 'campname']).max().reset_index() #TODO: right now we just keep the max number of days by instructional track. After I get the defn of tracks, can/should change this.
    cdays = cdays[['district', 'distname', 'campus', 'campname', 'days']]

    ddays = cdays.groupby(by=['district', 'distname']).agg({'days': ['min', 'mean', 'max']}).reset_index()
    ddays.columns = [' '.join(col).strip() for col in ddays.columns.values]
    ddays = ddays.rename({'days min': 'days_min', 'days mean': 'days_mean', 'days max': 'days_mean'}, axis='columns')

    days = cdays.merge(ddays, on = ['district', 'distname'])
    return days