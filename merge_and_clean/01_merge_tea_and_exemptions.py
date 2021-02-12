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

SET_DOI_DATE = clean_final.prioritize_term_date

# %% Set treatment status

laws["doi_date"] = SET_DOI_DATE(data=laws).doi_date

# doi_year is year of first treated test - occurs in march
laws["doi_year"] = (
    laws["doi_date"]
    .apply(pd.to_datetime)
    .apply(lambda x: clean_final.next_month(x, month=3, day=29))
)


# %% Limit analytic sample to pre 2020 dois (treated as non-dois)
laws = laws[(laws.doi_year < 2020) | (laws.doi_year.isnull())]

# %% School-Level

data_school = clean_for_merge.merge_school_and_exemptions(
    tea_df=tea_school, laws_df=laws, teacher_df=teachers, geo_df=geo
)
data_school = clean_final.destring_vars(data_school)
data_school = clean_final.gen_exempt_categories(data_school)
data_school = clean_final.gen_student_vars(data_school)
data_school = clean_final.gen_district_vars(data_school)
data_school = clean_final.gen_teacher_vars(data_school)
data_school = clean_final.gen_score_vars(data_school)
data_school = clean_final.gen_gdid_vars(data_school)
data_school = clean_final.gen_event_vars(data_school)
data_school = clean_final.gen_certification_vars(data_school)
data_school = clean_final.gen_hte_chars_vars(data_school, "campus")
data_school = clean_final.gen_eligiblity(data_school, 2019, "eligiblity19", "campus")

data_school.to_csv(
    os.path.join(start.data_path, "clean", "master_data_school.csv"), sep=","
)

# %% District-level
data_district = clean_for_merge.merge_district_and_exemptions(
    tea_df=tea_district, laws_df=laws, geo_df=geo
)
data_district = clean_final.destring_vars(data_district)
data_district = clean_final.gen_exempt_categories(data_district)
data_district = clean_final.gen_student_vars(data_district)
data_district = clean_final.gen_district_vars(data_district)
data_district = clean_final.gen_teacher_vars(data_district)
data_district = clean_final.gen_score_vars(data_district)
data_district = clean_final.gen_gdid_vars(data_district)
data_district = clean_final.gen_event_vars(data_district)

data_district = clean_final.gen_district_vars(data_district)
data_district = clean_final.gen_hte_chars_vars(data_district, "district")
data_district = clean_final.gen_eligiblity(
    data_district, 2019, "eligible19", "district"
)


# generate max and min for district
district_max = (
    data_school[["district", "campus", "year", "avescores"]]
    .groupby(["district", "year"])["avescores"]
    .max()
    .reset_index()
)
district_min = (
    data_school[["district", "campus", "year", "avescores"]]
    .groupby(["district", "year"])["avescores"]
    .min()
    .reset_index()
)
district_spread = district_max.rename(columns={"avescores": "max_school_avescore"})
district_spread = district_spread.merge(district_min).rename(
    columns={"avescores": "min_school_avescore"}
)
district_spread["school_spread"] = (
    district_spread.max_school_avescore - district_spread.min_school_avescore
)
data_district = data_district.merge(
    district_spread,
    left_on=["district", "year"],
    right_on=["district", "year"],
    how="left",
)

data_district.to_csv(
    os.path.join(start.data_path, "clean", "master_data_district.csv"), sep=","
)

# %% GDID
cols = [c for c in data_school.columns if c.lower()[:3] != "reg"]
gdid_school = data_school[cols]

# Limit Sample
gdid_school = gdid_school[gdid_school.distischarter == 0]
gdid_school = gdid_school[(gdid_school.doi)]
gdid_school = gdid_school[
    (gdid_school.doi_year < 2020) & (gdid_school.doi_year >= 2017)
]

gdid_school.to_csv(os.path.join(start.data_path, "clean", "gdid_school.csv"), sep=",")

# %% Subject-Grade-Level

subjects = [col for col in list(gdid_school.columns) if col.endswith("std")]
reshape = gdid_school[["campus", "year"] + subjects]
reshape = pd.melt(reshape, id_vars=["campus", "year"])
reshape = reshape.rename(columns={"variable": "test", "value": "score_std"})
reshape = reshape.dropna(axis=0)


subject_grade = reshape.merge(
    gdid_school, left_on=["campus", "year"], right_on=["campus", "year"]
)

math_tests = [
    "m_3rd_std",
    "m_4th_std",
    "m_5th_std",
    "m_6th_std",
    "m_7th_std",
    "m_8th_std",
    "alg_std",
]

reading_tests = [
    "r_3rd_std",
    "r_4th_std",
    "r_5th_std",
    "r_6th_std",
    "r_7th_std",
    "r_8th_std",
    "eng1_std",
]

subject_grade["math_test"] = np.where(subject_grade.test.isin(math_tests), 1, 0)

subject_grade["reading_test"] = np.where(subject_grade.test.isin(reading_tests), 1, 0)

subject_grade["test_by_year"] = subject_grade["test"] + subject_grade["year"].astype(
    str
)
subject_grade.to_csv(
    os.path.join(start.data_path, "clean", "gdid_subject.csv"), sep=","
)


# %%
