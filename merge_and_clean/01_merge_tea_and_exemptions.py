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


# %% School-Level

data_school = clean_for_merge.merge_school_and_exemptions(
    tea_df=tea_school, laws_df=laws, teacher_df=teachers, geo_df=geo
)
data_school = clean_final.destring_vars(data_school)
data_school = clean_final.gen_exempt_categories(data_school)
data_school = clean_final.gen_student_vars(data_school)
data_school = clean_final.gen_district_vars(data_school)
data_school = clean_final.gen_teacher_vars(data_school)
data_school = clean_final.gen_certification_vars(data_school)

data_school = clean_final.gen_score_vars(data_school)
data_school = clean_final.gen_gdid_vars(data_school)
data_school = clean_final.gen_event_vars(data_school)
data_school = clean_final.generate_pretreatment_variables(data_school, "campus", 2015)
data_school["eligiblity19"] = clean_final.gen_eligiblity(
    data_school, eligible_indicator="eligible", level="campus", eligibility_year=2019
)

data_school["analytic_sample"] = clean_final.gen_analysis_sample(
    data_school, 2016, 2019
)
data_school = data_school[[c for c in data_school.columns if c.lower()[:3] != "reg"]]

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
data_district = clean_final.generate_pretreatment_variables(
    data_district, "district", 2015
)
data_district["eligiblity19"] = clean_final.gen_eligiblity(
    data_district,
    eligible_indicator="eligible",
    level="district",
    eligibility_year=2019,
)
data_district["analytic_sample"] = clean_final.gen_analysis_sample(
    data_district, 2016, 2019
)
data_district["score_range"] = clean_final.generate_district_spread(
    district_data=data_district,
    school_data=data_school,
    outcome="avescores",
    groupby=["district", "year"],
)
data_district = data_district[
    [c for c in data_district.columns if c.lower()[:3] != "reg"]
]

data_district.to_csv(
    os.path.join(start.data_path, "clean", "master_data_district.csv"), sep=","
)

# %% GDID
cols = [c for c in data_school.columns if c.lower()[:3] != "reg"]
gdid_school = data_school[cols]

# Limit Sample
gdid_school = gdid_school[(gdid_school.doi)]
gdid_school.to_csv(os.path.join(start.data_path, "clean", "gdid_school.csv"), sep=",")

# %% Subject-Grade-Level

subjects_std = [col for col in list(data_school.columns) if col.endswith("_std")]
reshape_std = data_school[["campus", "year"] + subjects_std]
reshape_std = pd.melt(reshape_std, id_vars=["campus", "year"])
reshape_std = reshape_std.rename(columns={"variable": "test", "value": "score_std"})
reshape_std = reshape_std.dropna(axis=0)
reshape_std["test"] = reshape_std.test.str.replace("_std", "")

subjects_yr15std = [
    col + "_yr15std" for col in clean_final.aggregate_variables["avescores"]
]
reshape_yr15std = data_school[["campus", "year"] + subjects_yr15std]
reshape_yr15std = pd.melt(reshape_yr15std, id_vars=["campus", "year"])
reshape_yr15std = reshape_yr15std.rename(
    columns={"variable": "test", "value": "score_yr15std"}
)
reshape_yr15std = reshape_yr15std.dropna(axis=0)
reshape_yr15std["test"] = reshape_yr15std.test.str.replace("_yr15std", "")


subject_grade = reshape_std.merge(
    reshape_yr15std,
    left_on=["campus", "year", "test"],
    right_on=["campus", "year", "test"],
)
subject_grade = subject_grade.merge(
    data_school, left_on=["campus", "year"], right_on=["campus", "year"]
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
