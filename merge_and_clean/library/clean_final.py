import pandas as pd
import numpy as np
import datetime

from dofis.merge_and_clean.library import start
from dofis.merge_and_clean.library import clean_for_merge


def gen_doi_date(data: pd.DataFrame):
    """returns datetime for doi plan implementation

    if there is a term date, (i.e. "plan will be in effect \
        from August 2017 to August 2022") that date is preffered. \
        if no month is given, assume August. If no term date, \
        we use the date a plan was finalized (i.e. "August, 5, 2018 - \
        Board voted to approve DOI plan.")

    Args:
        data (pd.DataFrame): Dataframe which contains district name (distname)\
        term_year, term_month, finalize_year, and finalize month. 

    Returns:
        [pd.DataFrame]: Contains district and doi datetime
    """
    dates = pd.DataFrame()

    dates['distname'] = data.distname
    dates['doi_year'] = data.term_year
    dates['doi_month'] = data.term_month
    dates.loc[(data['term_month'].isna()) & (
        ~dates['doi_year'].isna()), 'doi_month'] = 'August'

    # If missing, go with finalize date
    dates.loc[dates['doi_year'].isna(), 'doi_month'] = data.finalize_month
    dates.loc[dates['doi_year'].isna(), 'doi_year'] = data.finalize_year

    dates['day'] = 1
    months_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4,
                   'May': 5, 'June': 6, 'July': 7, 'August': 8,
                   'September': 9, 'October': 10, 'November': 11,
                   'December': 12}
    dates['month'] = dates['doi_month'].map(months_dict)
    dates['year'] = dates['doi_year']
    dates['doi_date'] = pd.to_datetime(dates[['year', 'month', 'day']])

    return dates


def next_month(date: datetime.datetime, month: int, day: int) -> int:
    """Get the year of the next month that matches passed argument

    Args:
        date (datetime.datetime): [current date]
        month (int): [month of interest]
        day (int): [day in month of interest]

    Returns:
        int: [year of month of interest]
    """
    # Treated if plan is implemented before March of year
# (first possible testing date)
    if date.month < month or (date.month == month and date.day < day):
        return date.year
    return date.year + 1


def gen_vars(data):
    data = destring_vars(data)
    data = gen_exempt_categories(data)
    data = gen_student_vars(data)
    data = gen_district_vars(data)
    data = gen_teacher_vars(data)
    data = gen_score_vars(data)
    data = gen_gdid_vars(data)
    data = gen_event_vars(data)
    return data


def destring_vars(data):
    data['distischarter'] = np.where(data.distischarter == "Y", "1", "0")

    num_cols = ['teachers_nodegree_num', 'teachers_badegree_num',
                'teachers_msdegree_num', 'teachers_phddegree_num',
                'teachers_num', 'teachers_exp_ave',
                'teachers_tenure_ave', 'teachers_turnover_ratio_d',
                'stu_teach_ratio', 'distischarter']
    for col in list(data.columns):
        if col.startswith('class_size') or col.startswith('perf'):
            num_cols.append(col)
    print(num_cols)
    data[num_cols] = data[num_cols].apply(pd.to_numeric, errors='coerce')

    return data


def gen_exempt_categories(data):
    data['exempt_firstday'] = np.where(data['reg25_0811'] == 1, 1, 0)
    data['exempt_minutes'] = np.where(data['reg25_081'] == 1, 1, 0)
    data['exempt_lastday'] = np.where(data['reg25_0812'] == 1, 1, 0)
    data['exempt_certification'] = np.where(((data['reg21_003'] == 1) |
                                             (data['reg21_057'] == 1) |
                                             (data['reg21_053'] == 1)),
                                            1, 0)
    data['exempt_probation'] = np.where(data['reg21_102'] == 1, 1, 0)
    data['exempt_servicedays'] = np.where(data['reg21_401'] == 1, 1, 0)
    data['exempt_eval'] = np.where(data['reg21_352'] == 1, 1, 0)
    data['exempt_classsize'] = np.where(((data['reg25_112'] == 1) |
                                         (data['reg25_113'] == 1)),
                                        1, 0)
    data['exempt_attendance'] = np.where(data['reg25_092'] == 1, 1, 0)
    data['exempt_behavior'] = np.where(data['reg37_0012'] == 1, 1, 0)

    return data


def gen_student_vars(data):
    data['students_frpl'] = data['students_frpl_num'] / data['students_num']
    data['students_black'] = data['students_black_num'] / data['students_num']
    data['students_hisp'] = data['students_hisp_num'] / data['students_num']
    data['students_white'] = data['students_white_num'] / data['students_num']
    data['students_ell'] = data['students_ell_num'] / data['students_num']
    data['students_sped'] = data['students_sped_num'] / data['students_num']
    data['students_cte'] = data['students_cte_num'] / data['students_num']

    data['days'] = data['perf_studays']/data['students_num']
    

    data['students_teacher_ratio'] = data.students_num / data.teachers_num

    return data

# District Characteristics


def gen_district_vars(data):
    data['charter'] = np.where((data['distischarter'] == "Y"), True, False)

    tps_districts = ((data['doi'] is False) & (~data['charter']))

    data['district_status'] = np.where(tps_districts, 'tps',
                                       np.where((data['doi']), 'doi',
                                                np.where((data['charter']),
                                                         'charter', '')))

    # Geography indicators
    geography = {'A': 'Urban', 'C': 'Urban',
                 'B': 'Suburban', 'D': 'Suburban',
                 'E': 'Town', 'F': 'Town', 'G': 'Town',
                 'H': 'Rural'}
    data['geography'] = data['type'].map(geography)
    data['type_urban'] = np.where(data['geography'] == 'Urban', 1, 0)
    data['type_suburban'] = np.where(data['geography'] == 'Suburban', 1, 0)
    data['type_town'] = np.where(data['geography'] == 'Town', 1, 0)
    data['type_rural'] = np.where(data['geography'] == 'Rural', 1, 0)

    data['eligible'] = np.where((data.distischarter == 'Y') | (
        data.rating_academic == 'F') | (data.rating_financial == 'Fail'), 0, 1)

    return data


def gen_teacher_vars(data):
    #  Teacher Characteristics
    data['teachers_nodegree'] = data['teachers_nodegree_num'] / \
        data['teachers_num']
    data['teachers_badegree'] = data['teachers_badegree_num'] / \
        data['teachers_num']
    data['teachers_msdegree'] = data['teachers_msdegree_num'] / \
        data['teachers_num']
    data['teachers_phddegree'] = data['teachers_phddegree_num'] / \
        data['teachers_num']

    return data


def gen_score_vars(data):

    data = clean_for_merge.standardize_scores_within_year(data=data)

    elem_math = ['m_3rd_std', 'm_4th_std', 'm_5th_std']
    elem_reading = ['r_3rd_std', 'r_4th_std', 'r_5th_std']
    elem = ['m_3rd_std', 'm_4th_std', 'm_5th_std',
            'r_3rd_std', 'r_4th_std', 'r_5th_std']
    middle_math = ['m_6th_std', 'm_7th_std', 'm_8th_std']
    middle_reading = ['r_6th_std', 'r_7th_std', 'r_8th_std']
    middle_science = ['s_8th_std']
    algebra = ['alg_std']
    biology = ['bio_std']
    eng1 = ['eng1_std']
    math = ['m_3rd_std', 'm_4th_std', 'm_5th_std', 'm_6th_std',
            'm_7th_std', 'm_8th_std',
            'alg_std']
    reading = ['r_3rd_std', 'r_4th_std', 'r_5th_std',
               'r_6th_std', 'r_7th_std', 'r_8th_std',
               'eng1_std']
    all_scores = ['m_3rd_std', 'm_4th_std', 'm_5th_std',
                  'm_6th_std', 'm_7th_std', 'm_8th_std',
                  'r_3rd_std', 'r_4th_std', 'r_5th_std',
                  'r_6th_std', 'r_7th_std', 'r_8th_std',
                  's_8th_std',
                  'alg_std', 'bio_std']

    data['elem_math'] = data[elem_math].mean(axis=1)
    data['elem_reading'] = data[elem_reading].mean(axis=1)
    data['elem'] = data[elem].mean(axis=1)

    data['middle_math'] = data[middle_math].mean(axis=1)
    data['middle_reading'] = data[middle_reading].mean(axis=1)
    data['middle_science'] = data[middle_science].mean(axis=1)

    data['algebra'] = data[algebra].mean(axis=1)
    data['biology'] = data[biology].mean(axis=1)
    data['eng1'] = data[eng1].mean(axis=1)

    data['math'] = data[math].mean(axis=1)
    data['reading'] = data[reading].mean(axis=1)
    data['avescores'] = data[all_scores].mean(axis=1)

    return data


def gen_eligiblity(data, year, varname, level):

    datayear = data[data.year == 2019]
    datayear = datayear[[level, 'eligible']]
    datayear = datayear.rename({'eligible': varname}, axis=1)

    data = data.merge(datayear,
                      how='left',
                      left_on=[level],
                      right_on=[level],
                      validate='m:1')
    return data


def gen_analysis_sample(data,
                        min_doi_year,
                        max_doi_year):
    data['pre2020_dois'] = np.where((data.doi == True), True, False)
    data['pre2020_dois'] = np.where(data.doi_year > min_doi_year, data.pre2020_dois, False)
    data['pre2020_dois'] = np.where(data.doi_year < max_doi_year, data.pre2020_dois, False)

    return data




# Specification variables
def gen_gdid_vars(data):
    data['treatpost'] = np.where(
        ((data.year >= data.doi_year) & (data.doi)), True, False)
    data['yearpost'] = np.where(
        data.year >= data.doi_year, data.year - data.doi_year, 0)  # phase-in
    data['yearpre'] = np.where(
        data.year <= data.doi_year, data.year - data.doi_year, 0)  # pre-trend
    data['yearpre'] = np.where(
        data.yearpre <= -5, -5, data.yearpre)  # pre-trend effect
    return data


def gen_event_vars(data):
    # Non-parametric fixed effects for years pre and post - pre# and post#
    data['pre5'] = np.where(data.yearpre <= -5, 1, 0)
    data['pre4'] = np.where(data.yearpre == -4, 1, 0)
    data['pre3'] = np.where(data.yearpre == -3, 1, 0)
    data['pre2'] = np.where(data.yearpre == -2, 1, 0)
    data['pre1'] = np.where(data.yearpre == -1, 1, 0)
    data['post1'] = np.where((data.yearpost == 0) &
                             (data.treatpost == 1), 1, 0)
    data['post2'] = np.where(data.yearpost == 1, 1, 0)
    data['post3'] = np.where(data.yearpost == 2, 1, 0)
    return data


def gen_hte_chars_vars(data: pd.DataFrame, level_index: str):

    data_pre = data.loc[data.year == 2016]
    data_pre = data_pre.rename(columns={'students_hisp': 'pre_hisp',
                                        'students_ell': 'pre_ell',
                                        'students_white': 'pre_white',
                                        'students_black': 'pre_black',
                                        'students_sped': 'pre_sped',
                                        'students_frpl': 'pre_frpl',
                                        'avescores': 'pre_avescore',
                                        'students_num': 'pre_num',
                                        'teachers_exp': 'pre_exp',
                                        'teachers_turnover_ratio_d': 'pre_turnover',
                                        'teachers_tenure_ave': 'pre_tenure',
                                        'students_teacher_ratio': 'pre_ratio'})
    for var in ['pre_hisp', 'pre_ell', 'pre_white', 'pre_black',
                'pre_sped', 'pre_num', 'pre_turnover', 'pre_avescore']:
        for p in [.25, .5, .75, 1]:
            num = str(int(p * 100))
            newvar = var + num
            if p == .25:
                data_pre[newvar] = np.where(
                    data_pre[var] <= data_pre[var].quantile(p), 1, 0)
            if p > .25:
                lp = p - .25
                data_pre[newvar] = np.where(((data_pre[var] > data_pre[var].quantile(lp)) &
                                             (data_pre[var] <= data_pre[var].quantile(p))), 1, 0)
    variables = [level_index]
    variables = variables + (list(data_pre.filter(regex=("pre_"))))
    data_pre = data_pre[variables]
    data_pre_geo_vars = [level_index, 'type_urban',
                         'type_suburban', 'type_town', 'type_rural']
    data_pre_geo = data[data.year == 2016][data_pre_geo_vars]
    data_pre = data_pre.merge(data_pre_geo, how='left', left_on=[
                              level_index], right_on=[level_index],
                              validate='one_to_one')
    data_pre = data_pre.rename(columns={'type_urban': 'pre_urban',
                                        'type_suburban': 'pre_suburban',
                                        'type_town': 'pre_town',
                                        'type_rural': 'pre_rural'})
    data_pre['pre_turnover'] = data_pre.pre_turnover / 100
    data = data.reset_index().merge(data_pre, left_on=level_index,
                                    right_on=level_index, how='left',
                                    validate='m:1')

    return data
