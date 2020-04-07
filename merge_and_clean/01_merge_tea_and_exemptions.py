import os
import pandas as pd
import numpy as np
import datetime

pd.options.display.max_columns = 200
try:
    from merge_and_clean.library import clean_for_merge
    from merge_and_clean.library import clean_final
except:
    from library import start
    from library import clean_for_merge
    from library import clean_final
    


###
#   Import
###
laws = clean_for_merge.import_laws()
geo = clean_for_merge.import_geo()
tea_district = clean_for_merge.import_tea_district()
tea_school = clean_for_merge.import_tea_school()
teachers_district =  pd.read_csv(os.path.join(start.data_path, 'tea', 'teachers_d_long.csv'),
            sep=",", low_memory = False)
teachers_schools = pd.read_csv(os.path.join(start.data_path, 'tea', 'teachers_c_long.csv'),
            sep=",", low_memory = False)


###
#   Define doi_year
###
# Treated if plan is implemented before March of year (first possible testing date)
def next_march(date):
    if date.month == 3:
        year = date.year
    while date.month != 3:
        date = date + datetime.timedelta(days = + 32)
        year = date.year

def next_month(date: datetime.datetime, month: int, day: int) -> int:
    """Get the year of the next month matching passed argument."""
    
    if date.month < month or (date.month == month and date.day < day):
        return date.year
    return date.year + 1
# doi_year is year of treated test
laws['doi_year'] = laws['doi_date'].apply(pd.to_datetime).apply(lambda x: next_month(x, month=3, day=29))


###
#   School-level
###
tea_school, laws = clean_for_merge.resolve_merge_errors(tea_school, laws)
# TODO: add back teachers
data_school = tea_school.merge(laws, left_on='distname', right_on='distname', how='left', indicator=True)
data_school.loc[(data_school['_merge'] == 'both'), 'doi'] = True
data_school.loc[(data_school['_merge'] == 'left_only'), 'doi'] = False
data_school = data_school.merge(geo, left_on='cntyname', right_on='county', how='left', indicator=False)
data_school = data_school.merge(teachers_schools, left_on = ['district', 'campus', 'year'], right_on = ['district', 'campus', 'year'], how = 'left', indicator = '_teacher_merge')

print(laws.distname.nunique(), tea_school.distname.nunique(), data_school.distname.nunique())
print(tea_school.campus.nunique(), data_school.campus.nunique())

data_school = clean_final.gen_vars(data_school)

data_school.to_csv(os.path.join(start.data_path, 'clean', 'master_data_school.csv'),
    sep=",")

# generate max and min for district
#district_spread = data_school[['district', 'year']]
district_max = data_school[['district', 'campus', 'year', 'avescores']].groupby(['district', 'year'])['avescores'].max().reset_index()
district_min = data_school[['district', 'campus', 'year', 'avescores']].groupby(['district', 'year'])['avescores'].min().reset_index()
district_spread = district_max.rename(columns = {'avescores': 'max_school_avescore'})
district_spread = district_spread.merge(district_min).rename(columns = {'avescores': 'min_school_avescore'})
district_spread['school_spread'] = district_spread.max_school_avescore - district_spread.min_school_avescore

###
#   District-level
###
tea_district, laws = clean_for_merge.resolve_merge_errors(tea_district, laws)
data_district = tea_district.merge(laws, left_on='distname', right_on='distname', how='left', indicator=True)
data_district.loc[(data_district['_merge'] == 'both'), 'doi'] = True
data_district.loc[(data_district['_merge'] == 'left_only'), 'doi'] = False
data_district = data_district.merge(geo, left_on='cntyname', right_on='county', how='left', indicator=False)
data_district = data_district.merge(teachers_district, left_on = ['district', 'year'], right_on = ['district', 'year'], how = 'left', indicator = False)
print(laws.distname.nunique(), tea_district.distname.nunique(), data_district.distname.nunique())
data_district = clean_final.gen_vars(data_district)
data_district = clean_final.gen_gdid_vars(data_district)
data_district = clean_final.gen_event_vars(data_district)
data_district = data_district.merge(district_spread, left_on = ['district', 'year'], right_on = ['district', 'year'], how = 'left')
data_district.to_csv(os.path.join(start.data_path, 'clean', 'master_data_district.csv'),
    sep=",")


###
# GDID - School
###
data_gdid = data_school[data_school.doi == True]
cols = [c for c in data_gdid.columns if c.lower()[:3] != 'reg']
data_gdid = data_gdid[cols]
data_gdid['doi_year'] = np.where((data_gdid.doi_year == 2016), np.nan, data_gdid.doi_year) #drop first implementer (three districts)
data_gdid['doi_year'] = np.where((data_gdid.doi_year == 2020), np.nan, data_gdid.doi_year) #drop last implementers (14 districts) Can add after updating dataset
data_gdid = data_gdid[pd.notnull(data_gdid.doi_year)]

# generate specifcation variables
data_gdid = clean_final.gen_gdid_vars(data_gdid)
data_gdid = clean_final.gen_event_vars(data_gdid)

data_gdid.to_csv(os.path.join(start.data_path, 'clean', 'gdid.csv'), sep=",")

###
# Subject-Grade-Level
###
subjects = (list(data_gdid.filter(regex = ("_avescore"))))
variables = ['district', 'campus', 'year'] + subjects
reshape = data_gdid[variables]
reshape = pd.melt(reshape, id_vars = ['district', 'campus', 'year'])
reshape = reshape.rename(columns = {'variable': 'test', 'value': 'score'})
reshape = reshape.dropna(axis = 0)

# standardize
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
reshape = reshape[['district', 'campus', 'year', 'test', 'score', 'score_std']]


subject_grade = reshape.merge(data_gdid, left_on = ['district','campus', 'year'], right_on = ['district', 'campus', 'year'])
subject_grade = subject_grade[(subject_grade.test != 'eng2_avescore') & (subject_grade.test != 'us_avescore') & (subject_grade.test != 's_8th_avescore')]

# test year fixed effects and test indicator
subject_grade['test_by_year'] = subject_grade['test'] + subject_grade['year'].map(str) # subject-year fixed effects
math_tests = ['m_3rd_avescore', 'm_4th_avescore', 'm_5th_avescore',
              'm_6th_avescore', 'm_7th_avescore', 'm_8th_avescore', 'alg_avescore']
reading_tests = ['r_3rd_avescore', 'r_4th_avescore', 'r_5th_avescore',
              'r_6th_avescore', 'r_7th_avescore', 'r_8th_avescore', 'eng1_avescore']
subject_grade['math'] = np.where(np.isin(subject_grade.test, math_tests), 1, 0)
subject_grade['reading'] = np.where(np.isin(subject_grade.test, reading_tests), 1, 0)

# save
subject_grade.to_csv(os.path.join(start.data_path, 'clean', 'gdid_subject.csv'), sep=",")
