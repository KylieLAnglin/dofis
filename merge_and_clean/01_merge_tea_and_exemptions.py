# %%
import os

import numpy as np
import pandas as pd

from dofis.merge_and_clean.library import clean_final
from dofis.merge_and_clean.library import clean_for_merge
from dofis import start

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
laws = laws[laws.doi_year < 2023]  # drop 2023 implementers, not yet 2023

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
data_school["eligible19"] = clean_final.gen_eligiblity(
    data_school, eligible_indicator="eligible", level="campus", eligibility_year=2019
)

# data_school["analytic_sample"] = clean_final.gen_analysis_sample(
#     data=data_school, min_doi_year=2017, max_doi_year=2019
# )
data_school = data_school[[c for c in data_school.columns if c.lower()[:3] != "reg"]]
data_school["group"] = clean_final.gen_analytic_group(data=data_school)

data_school.to_csv(
    os.path.join(start.DATA_PATH, "clean", "master_data_school.csv"), sep=","
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
data_district = clean_final.gen_score_vars(data_district, level="district")
data_district = clean_final.gen_gdid_vars(data_district)
data_district = clean_final.gen_event_vars(data_district)

data_district = clean_final.gen_district_vars(data_district)
data_district = clean_final.generate_pretreatment_variables(
    data_district, "district", 2015
)
data_district["eligible19"] = clean_final.gen_eligiblity(
    data_district,
    eligible_indicator="eligible",
    level="district",
    eligibility_year=2019,
)
data_district["analytic_sample"] = clean_final.gen_analysis_sample(
    data=data_district, min_doi_year=2017, max_doi_year=2019
)
data_district["score_range"] = clean_final.generate_district_spread(
    district_data=data_district,
    school_data=data_school,
    outcome="avescores",
    groupby=["district", "year"],
)

data_district["group"] = clean_final.gen_analytic_group(data=data_district)

# data_district = data_district[
#     [c for c in data_district.columns if c.lower()[:3] != "reg"]
# ]

data_district.to_csv(
    os.path.join(start.DATA_PATH, "clean", "master_data_district.csv"), sep=","
)

# %%
