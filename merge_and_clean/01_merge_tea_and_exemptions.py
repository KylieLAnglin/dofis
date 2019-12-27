import os
import pandas as pd
import numpy as np

pd.options.display.max_columns = 200
from merge_and_clean.library import start
from merge_and_clean.library import clean_for_merge

def gen_vars(data):
    # # Convert strings to numeric
    try:
        num_cols = ['teachers_nodegree_num', 'teachers_badegree_num', 'teachers_msdegree_num', 'teachers_phddegree_num',
            'teachers_num', 'teachers_exp_ave',
            'teachers_tenure_ave', 'teachers_turnover_ratio', 'stu_teach_ratio']
        data[num_cols] = data[num_cols].apply(pd.to_numeric, errors='coerce')
    except:
        num_cols = ['teachers_nodegree_num', 'teachers_badegree_num', 'teachers_msdegree_num', 'teachers_phddegree_num',
        'teachers_num', 'teachers_exp_ave',
        'teachers_tenure_ave', 'teachers_turnover_ratio_d', 'stu_teach_ratio']
        data[num_cols] = data[num_cols].apply(pd.to_numeric, errors='coerce')

    # Student characteristics

    data['students_frpl'] = data['students_frpl_num'] / data['students_num']
    data['students_black'] = data['students_black_num'] / data['students_num']
    data['students_hisp'] = data['students_hisp_num'] / data['students_num']
    data['students_white'] = data['students_white_num'] / data['students_num']
    data['students_ell'] = data['students_ell_num'] / data['students_num']
    data['students_sped'] = data['students_sped_num'] / data['students_num']
    data['students_cte'] = data['students_cte_num'] / data['students_num']

    data['students_teacher_ratio'] = data['students_num'] / data['teachers_num']
# District Characteristics

    geography = {'A': 'Urban', 'C': 'Urban',
            'B': 'Suburban', 'D': 'Suburban',
            'E': 'Town', 'F': 'Town', 'G': 'Town',
            'H': 'Rural'}
    data['geography'] = data['type'].map(geography)

    data['charter'] = np.where((data['distischarter'] == "Y"), True, False)

    data['district_status'] = np.where((data['doi'] == False) & (data['charter'] == False), 'tps',
                                np.where((data['doi'] == True), 'doi',
                                        np.where((data['charter'] == True), 'charter', 'missing')))


    # Geography indicators
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

    #  Teacher Characteristics
    data['teachers_nodegree'] = data['teachers_nodegree_num'] / data['teachers_num']
    data['teachers_badegree'] = data['teachers_badegree_num'] / data['teachers_num']
    data['teachers_msdegree'] = data['teachers_msdegree_num'] / data['teachers_num']
    data['teachers_phddegree'] = data['teachers_phddegree_num'] / data['teachers_num']

    return data

def gen_vars_scores(data):
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
    math = ['m_3rd_std', 'm_4th_std', 'm_5th_std', 'm_6th_std', 'm_7th_std', 'm_8th_std']
    reading = ['r_3rd_std', 'r_4th_std', 'r_5th_std', 'r_6th_std', 'r_7th_std', 'r_8th_std']

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

    data['math'] = data[math].mean(axis = 1)
    data['reading'] = data[reading].mean(axis = 1)

    data['avescores'] = data[all_scores].mean(axis=1)

    return data

###
#   Import
###
laws = clean_for_merge.import_laws()
geo = clean_for_merge.import_geo()
tea_district = clean_for_merge.import_tea_district()
tea_school = clean_for_merge.import_tea_school()
teachers = clean_for_merge.import_teachers()


###
#   District-level
###
tea_district, laws = clean_for_merge.resolve_merge_errors(tea_district, laws)
data_district = tea_district.merge(laws, left_on='distname', right_on='distname', how='left', indicator=True)
data_district.loc[(data_district['_merge'] == 'both'), 'doi'] = True
data_district.loc[(data_district['_merge'] == 'left_only'), 'doi'] = False
data_district = data_district.merge(geo, left_on='cntyname', right_on='county', how='left', indicator=False)
print(laws.distname.nunique(), tea_district.distname.nunique(), data_district.distname.nunique())
data_district = gen_vars(data_district)
data_district = gen_vars_scores(data_district)

#data_district['doi_year'] = np.where((data_district.doi_year == 2019), np.nan, data_district.doi_year) # set aside 2019 districts for now
data_district.to_csv(os.path.join(start.data_path, 'clean', 'master_data_district.csv'),
    sep=",")


###
#   School-level
###

tea_school, laws = clean_for_merge.resolve_merge_errors(tea_school, laws)
# add back teachers
data_school = tea_school.merge(laws, left_on='distname', right_on='distname', how='left', indicator=True)
data_school.loc[(data_school['_merge'] == 'both'), 'doi'] = True
data_school.loc[(data_school['_merge'] == 'left_only'), 'doi'] = False
data_school = data_school.merge(teachers, left_on = ['campus', 'year'], right_on = ['campus', 'year'], how = 'left')
data_school = data_school.merge(geo, left_on='cntyname', right_on='county', how='left', indicator=False)
print(laws.distname.nunique(), tea_school.distname.nunique(), data_school.distname.nunique())
print(tea_school.campus.nunique(), data_school.campus.nunique())

data_school = gen_vars(data_school)
data_school = gen_vars_scores(data_school)

#data['doi_year'] = np.where((data.doi_year == 2019), np.nan, data.doi_year) # set aside 2019 districts for now

data_school.to_csv(os.path.join(start.data_path, 'clean', 'master_data_school.csv'),
    sep=",")

###
# GDID
###
data_gdid = data_school[data_school.doi == True]
cols = [c for c in data_gdid.columns if c.lower()[:3] != 'reg']
data_gdid = data_gdid[cols]
data_gdid['doi_year'] = np.where((data_gdid.doi_year == 2015), np.nan, data_gdid.doi_year) #drop first implementer (one district)
#data['doi_year'] = np.where((data.doi_year == 2019), np.nan, data.doi_year) # set aside 2019 districts for now
data_gdid['treatpost'] = np.where(((data_gdid.year > data_gdid.doi_year) &(data_gdid.doi == True)), True, False)
data_gdid.to_csv(os.path.join(start.data_path, 'clean', 'gdid.csv'), sep=",")

###
# Subject-Grade-Level
###
subjects = (list(data_gdid.filter(regex = ("_avescore"))))
variables = ['campus', 'year'] + subjects
reshape = data_gdid[variables]
reshape = pd.melt(reshape, id_vars = ['campus', 'year'])
reshape = reshape.rename(columns = {'variable': 'test', 'value': 'score'})
reshape = reshape.dropna(axis = 0)

means = []
sds = []
for var in subjects:
    mean = reshape[(reshape.test == var) & (reshape.year == 2015)].score.mean()
    means.append(mean)
    sd = reshape[reshape.test == var].score.std()
    sds.append(sd)

means_sds = pd.DataFrame(list(zip(subjects, means, sds)), 
               columns =['test', 'test_mean', 'test_std']) 

reshape = reshape.merge(means_sds, left_on = 'test', right_on = 'test')
reshape['score_std'] = (reshape.score - reshape.test_mean)/reshape.test_std
reshape = reshape[['campus', 'year', 'test', 'score', 'score_std']]


subject_grade = reshape.merge(data_gdid, left_on = ['campus', 'year'], right_on = ['campus', 'year'])

subject_grade.to_csv(os.path.join(start.data_path, 'clean', 'gdid_subject.csv'), sep=",")
