# %%
import datetime
import os

import numpy as np
import pandas as pd

from library import clean_final, clean_for_merge, start

pd.options.display.max_columns = 200

# %%
tea_district = clean_for_merge.import_tea_district()
tea_school = clean_for_merge.import_tea_school()
laws = clean_for_merge.import_laws()
geo = clean_for_merge.import_geo()
teachers = clean_for_merge.import_teachers()

# Treated if plan is implemented before March of year
# (first possible testing date)


def next_month(date: datetime.datetime, month: int, day: int) -> int:
    """Get the year of the next month matching passed argument."""
    if date.month < month or (date.month == month and date.day < day):
        return date.year
    return date.year + 1


# doi_year is year of treated test
laws['doi_year'] = laws['doi_date'].apply(pd.to_datetime).apply(
    lambda x: next_month(x, month=3, day=29))


# %%
#   District-level

data_district = clean_for_merge.merge_district_and_exemptions(
    tea_df=tea_district, laws_df=laws, geo_df=geo)
data_district = clean_final.gen_vars(data_district)
data_district.to_csv(os.path.join(start.data_path, 'clean',
                                  'master_data_district.csv'), sep=",")

# %%
# School-Level
data_school = clean_for_merge.merge_school_and_exemptions(
    tea_df=tea_school, laws_df=laws, teacher_df=teachers, geo_df=geo)
data_school = clean_final.gen_vars(data_school)
data_school.to_csv(os.path.join(start.data_path, 'clean',
                                'master_data_school.csv'), sep=",")

# %%

# GDID

cols = [c for c in data_school.columns if c.lower()[:3] != 'reg']
gdid_school = data_school[cols]
# drop first implementer (one district)
gdid_school['doi_year'] = np.where(
    (gdid_school.doi_year == 2015), np.nan, gdid_school.doi_year)
# drop last implementers (14 districts)
gdid_school['doi_year'] = np.where(
    (gdid_school.doi_year == 2020), np.nan, gdid_school.doi_year)
gdid_school = gdid_school[gdid_school.distischarter == 0]
gdid_school.to_csv(os.path.join(
    start.data_path, 'clean', 'gdid_school.csv'), sep=",")

# %%
# Subject-Grade-Level

subjects = (list(gdid_school.filter(regex=("_avescore"))))
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

subject_grade.to_csv(os.path.join(
    start.data_path, 'clean', 'gdid_subject.csv'), sep=",")
