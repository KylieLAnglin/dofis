import pandas as pd
import numpy as np

try:
    from merge_and_clean.library import start
    from merge_and_clean.library import clean_for_merge
except:
    from library import start
    from library import clean_for_merge
    
def gen_vars(data):
    data = destring_vars(data)
    data = gen_student_vars(data)
    data = gen_district_vars(data)
    data = gen_teacher_vars(data)
    data = gen_score_vars(data)
    data = gen_gdid_vars(data)
    data = gen_event_vars(data)
    return data

def destring_vars(data):
    data['distischarter'] = np.where(data.distischarter == "Y", "1", "0")

    num_cols = ['teachers_nodegree_num', 'teachers_badegree_num', 'teachers_msdegree_num', 'teachers_phddegree_num',
    'teachers_num', 'teachers_exp_ave',
    'teachers_tenure_ave', 'teachers_turnover_ratio_d', 'stu_teach_ratio', 'distischarter']
    data[num_cols] = data[num_cols].apply(pd.to_numeric, errors='coerce')

    return data

def gen_student_vars(data):
    data['students_frpl'] = data['students_frpl_num'] / data['students_num']
    data['students_black'] = data['students_black_num'] / data['students_num']
    data['students_hisp'] = data['students_hisp_num'] / data['students_num']
    data['students_white'] = data['students_white_num'] / data['students_num']
    data['students_ell'] = data['students_ell_num'] / data['students_num']
    data['students_sped'] = data['students_sped_num'] / data['students_num']
    data['students_cte'] = data['students_cte_num'] / data['students_num']

    data['students_teacher_ratio'] = data['students_num'] / data['teachers_num']

    return data

# District Characteristics
def gen_district_vars(data):
    data['charter'] = np.where((data['distischarter'] == "Y"), True, False)

    data['district_status'] = np.where((data['doi'] == False) & (data['charter'] == False), 'tps',
                                np.where((data['doi'] == True), 'doi',
                                        np.where((data['charter'] == True), 'charter', 'missing')))


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

    data['eligible'] = np.where((data.distischarter == 'Y') | (data.rating_academic == 'F') |(data.rating_financial == 'Fail'), 0, 1)

    # Always eligible?
    #df_filter = data[['distname', 'year', 'eligible']]
    #df_filter = df_filter[~df_filter['year'].isin(['yr1112', 'yr1213', 'yr1314'])]
    #always_eligible = pd.DataFrame(df_filter.groupby(['distname'])['eligible'].min()).reset_index()
    #always_eligible.columns = ['distname', 'always_eligible']
    #data = data.merge(always_eligible.reset_index(), left_on='distname', right_on='distname', how='left')

    return data


def gen_teacher_vars(data):
    #  Teacher Characteristics
    data['teachers_nodegree'] = data['teachers_nodegree_num'] / data['teachers_num']
    data['teachers_badegree'] = data['teachers_badegree_num'] / data['teachers_num']
    data['teachers_msdegree'] = data['teachers_msdegree_num'] / data['teachers_num']
    data['teachers_phddegree'] = data['teachers_phddegree_num'] / data['teachers_num']

    return data


def gen_score_vars(data):
       # Performance

    # Standardize within subject using mean and standard deviation from 2014-15
    data = clean_for_merge.standardize_scores(data=data, std_year=2015)
    
    elem_math = ['m_3rd_std', 'm_4th_std', 'm_5th_std']
    elem_reading =  ['r_3rd_std', 'r_4th_std', 'r_5th_std']
    elem = ['m_3rd_std', 'm_4th_std', 'm_5th_std','r_3rd_std', 'r_4th_std', 'r_5th_std']
    middle_math = ['m_6th_std', 'm_7th_std', 'm_8th_std']
    middle_reading = ['r_6th_std', 'r_7th_std', 'r_8th_std']
    middle_science = ['s_8th_std']
    algebra = ['alg_std']
    biology = ['bio_std']
    eng1 = ['eng1_std']
    all_scores = ['m_3rd_std', 'm_4th_std', 'm_5th_std', 'm_6th_std', 'm_7th_std', 'm_8th_std',
            'r_3rd_std', 'r_4th_std', 'r_5th_std', 'r_6th_std', 'r_7th_std', 'r_8th_std',
            's_8th_std',
            'alg_std', 'bio_std']


    data['elem_math'] = data[elem_math].mean(axis=1)
    data['elem_reading'] = data[elem_reading].mean(axis=1)
    data['elem'] = data[elem].mean(axis=1)

    data['middle_math'] = data[middle_math].mean(axis=1)
    data['middle_reading'] = data[middle_reading].mean(axis = 1)
    data['middle_science'] = data[middle_science].mean(axis = 1)

    data['algebra'] = data[algebra].mean(axis = 1)
    data['biology'] = data[biology].mean(axis = 1)
    data['eng1'] = data[eng1].mean(axis = 1)

    data['avescores'] = data[all_scores].mean(axis=1)

    return data


## Specification variables
def gen_gdid_vars(data):
    data['treatpost'] = np.where(((data.year >= data.doi_year) &(data.doi == True)), True, False)
    data['yearpost'] = np.where(data.year >= data.doi_year, data.year - data.doi_year, 0) # phase-in effect
    data['yearpre'] = np.where(data.year <= data.doi_year, data.year - data.doi_year, 0) # pre-trend effect
    data['yearpre'] = np.where(data.yearpre <= -5, -5, data.yearpre) # pre-trend effect
    return data

def gen_event_vars(data):
    # Non-parametric fixed effects for years pre and post - pre# and post#
    data['pre5'] = np.where(data.yearpre <= -5, 1, 0)
    data['pre4'] = np.where(data.yearpre == -4, 1, 0)
    data['pre3'] = np.where(data.yearpre == -3, 1, 0)
    data['pre2'] = np.where(data.yearpre == -2, 1, 0)
    data['pre1'] = np.where(data.yearpre == -1, 1, 0)
    data['post1'] = np.where((data.yearpost == 0) & (data.treatpost == 1), 1, 0)
    data['post2'] = np.where(data.yearpost == 1, 1, 0)
    data['post3'] = np.where(data.yearpost == 2, 1, 0)
    return data