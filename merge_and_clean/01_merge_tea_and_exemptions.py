# %%
import datetime
import os

import numpy as np
import pandas as pd

from dofis.merge_and_clean.library import clean_final
from dofis.merge_and_clean.library import clean_for_merge
from dofis.merge_and_clean.library import start

pd.options.display.max_columns = 200

# %% Import
tea_district = clean_for_merge.import_tea_district()
tea_school = clean_for_merge.import_tea_school()
laws = clean_for_merge.import_laws()
geo = clean_for_merge.import_geo()
teachers = clean_for_merge.import_teachers()

# %% Set DOI date

# %% Set treatment status

laws['doi_date'] = clean_final.gen_doi_date(data=laws).doi_date

# doi_year is year of first treated test - occurs in march
laws['doi_year'] = laws['doi_date'].apply(pd.to_datetime).apply(
    lambda x: clean_final.next_month(x, month=3, day=29))


# %% Limit sample to pre 2020 dois
laws = laws[(laws.doi_year < 2020) | (laws.doi_year.isnull())]

# %% School-Level

data_school = clean_for_merge.merge_school_and_exemptions(
    tea_df=tea_school, laws_df=laws, teacher_df=teachers, geo_df=geo)
data_school = clean_final.gen_vars(data_school)
data_school = clean_final.gen_hte_chars_vars(data_school, 'campus')
data_school = clean_final.gen_eligiblity(data_school, 2019,
                                         'eligiblity19', 'campus')
data_school = clean_final.gen_analysis_sample(data=data_school,
                                              min_doi_year=2017,
                                              max_doi_year=2019)
data_school.to_csv(os.path.join(start.data_path, 'clean',
                                'master_data_school.csv'), sep=",")

# %% District-level
data_district = clean_for_merge.merge_district_and_exemptions(
    tea_df=tea_district, laws_df=laws, geo_df=geo)

data_district = clean_final.gen_vars(data_district)
data_district = clean_final.gen_district_vars(data_district)
data_district = clean_final.gen_hte_chars_vars(data_district, 'district')
data_district = clean_final.gen_eligiblity(data_district, 2019,
                                           'eligible19', 'district')
data_district = clean_final.gen_analysis_sample(data=data_district,
                                                min_doi_year=2017,
                                                max_doi_year=2019)


# generate max and min for district
district_max = data_school[['district', 'campus', 'year', 'avescores']].groupby(
    ['district', 'year'])['avescores'].max().reset_index()
district_min = data_school[['district', 'campus', 'year', 'avescores']].groupby(
    ['district', 'year'])['avescores'].min().reset_index()
district_spread = district_max.rename(
    columns={'avescores': 'max_school_avescore'})
district_spread = district_spread.merge(district_min).rename(
    columns={'avescores': 'min_school_avescore'})
district_spread['school_spread'] = district_spread.max_school_avescore - \
    district_spread.min_school_avescore
data_district = data_district.merge(district_spread,
                                    left_on=['district', 'year'],
                                    right_on=['district', 'year'],
                                    how='left')

# drop last implementers
# data_district['doi'] = np.where(data_district.doi_year == 2020,
#                                 False, data_district.doi)
# data_district['doi_year'] = np.where(data_district.doi_year == 2020,
#                                      np.nan, data_district.doi_year)
data_district.to_csv(os.path.join(start.data_path, 'clean',
                                  'master_data_district.csv'),
                     sep=",")

# %% GDID
cols = [c for c in data_school.columns if c.lower()[:3] != 'reg']
gdid_school = data_school[cols]
# drop first implementers (3 districts)
# gdid_school['doi_year'] = np.where(
#     (gdid_school.doi_year == 2016), np.nan, gdid_school.doi_year)

gdid_school = gdid_school[gdid_school.distischarter == 0]
#gdid_school = gdid_school[(gdid_school.doi_year < 2020) & (gdid_school.doi_year >= 2017)]
gdid_school.to_csv(os.path.join(
    start.data_path, 'clean', 'gdid_school.csv'), sep=",")

# %% Subject-Grade-Level

subjects = []
for col in list(gdid_school.columns):
    if col.endswith('_avescore') & ~col.startswith('pre'):
        print(col)
        subjects.append(col)
variables = ['campus', 'year'] + subjects
reshape = gdid_school[variables]
reshape = pd.melt(reshape, id_vars=['campus', 'year'])
reshape = reshape.rename(columns={'variable': 'test', 'value': 'score'})
reshape = reshape.dropna(axis=0)

means = []
sds = []
for var in subjects:
    mean = reshape[(reshape.test == var) & (reshape.year == 2015)].score.mean()
    means.append(mean)
    sd = reshape[reshape.test == var].score.std()
    sds.append(sd)

means_sds = pd.DataFrame(list(zip(subjects, means, sds)),
                         columns=['test', 'test_mean', 'test_std'])

reshape = reshape.merge(means_sds, left_on='test', right_on='test')
reshape['score_std'] = (reshape.score - reshape.test_mean)/reshape.test_std
reshape = reshape[['campus', 'year', 'test', 'score', 'score_std']]

subject_grade = reshape.merge(
    gdid_school, left_on=['campus', 'year'], right_on=['campus', 'year'])

math_tests = ['m_3rd_avescore', 'm_4th_avescore', 'm_5th_avescore',
              'm_6th_avescore', 'm_7th_avescore', 'm_8th_avescore',
              'alg_avescore']

reading_tests = ['r_3rd_avescore', 'r_4th_avescore', 'r_5th_avescore',
                 'r_6th_avescore', 'r_7th_avescore', 'r_8th_avescore',
                 'eng1_avescore']

subject_grade['math'] = np.where(subject_grade.test.isin(math_tests),
                                 1, 0)

subject_grade['reading'] = np.where(subject_grade.test.isin(reading_tests),
                                    1, 0)

subject_grade['test_by_year'] = subject_grade['test'] + \
    subject_grade['year'].astype(str)
subject_grade.to_csv(os.path.join(
    start.data_path, 'clean', 'gdid_subject.csv'), sep=",")


# %%
