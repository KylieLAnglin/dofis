#!/usr/bin/env python
# coding: utf-8

# %%


import os
import sys

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from openpyxl import load_workbook
from patsy import dmatrices
import statsmodels.api as sm

from dofis.analysis.library import start
from dofis.analysis.library import analysis

from sklearn.linear_model import LogisticRegression

# %%
POTENTIAL_COVARIATES = [
    "cnty_pop",
    "students_frpl",
    "students_black",
    "students_hisp",
    "students_white",
    "students_ell",
    "students_sped",
    "students_cte",
    "students_num",
    "students_num_d",
    "students_teacher_ratio",
    "type_urban",
    "type_suburban",
    "type_town",
    "type_rural",
    "teachers_nodegree",
    "teachers_badegree",
    "teachers_msdegree",
    "teachers_phddegree",
    "pre_turnover",
    "teachers_badegree_num",
    "teachers_exp_ave",
    "teachers_msdegree_num",
    "teachers_new_num",
    "teachers_nodegree_num",
    "teachers_num",
    "teachers_phddegree_num",
    "teachers_tenure_ave",
    "teachers_turnover_ratio_d",
    "math",
    "reading",
]


# %%
data = pd.read_csv(
    os.path.join(start.data_path, "clean", "master_data_school.csv"),
    sep=",",
    low_memory=False,
).set_index("campus")
data = data[data.doi_year != 2016]  # drop 3 early early adopters
data = data[data.distischarter == False]  # don't include charters
data["first_implementers"] = np.where(data.doi_year == 2017, 1, 0)
data["second_implementers"] = np.where(data.doi_year == 2018, 1, 0)
data["third_implementers"] = np.where(data.doi_year == 2019, 1, 0)


# %%
matching_df = data[data.year == 2016]  # match on last pre-treatment year
matching_df = matching_df[matching_df.second_implementers == 0]
matching_df = matching_df[matching_df.third_implementers == 0]
matching_df = matching_df[["first_implementers"] + POTENTIAL_COVARIATES]
matching_df = matching_df.dropna()

# %% Potential covariates
X = matching_df.drop(columns=["first_implementers"])
X = sm.add_constant(X)


# %%

mod = sm.OLS(matching_df.first_implementers, X.astype(float))
res = mod.fit_regularized(alpha=0.01, L1_wt=1, refit=True)
print(res.summary())

variables = []
for variable, coefficient in zip(list(X.columns), list(res.params)):
    if coefficient > 0:
        variables.append(variable)

# %%
mod = sm.OLS(matching_df.math, X.drop(columns=["math", "reading"]).astype(float))
res = mod.fit_regularized(alpha=0.01, L1_wt=1, refit=True)
print(res.summary())

for variable, coefficient in zip(list(X.columns), list(res.params)):
    if variable not in variables and coefficient > 0:
        variables.append(variable)
# %%
mod = sm.OLS(matching_df.reading, X.drop(columns=["math", "reading"]).astype(float))
res = mod.fit_regularized(alpha=0.01, L1_wt=1, refit=True)
print(res.summary())

for variable, coefficient in zip(list(X.columns), list(res.params)):
    if variable not in variables and coefficient > 0:
        variables.append(variable)

# %%
matching_df["const"] = 1
X = matching_df[variables]

mod = sm.Logit(matching_df.first_implementers, X.astype(float))
res = mod.fit()
print(res.summary())

# %%
matching_df["pscore"] = res.predict(X.astype(float))

# TOT weights
matching_df["ps_weight"] = matching_df.first_implementers + (
    1 - matching_df.first_implementers
) * matching_df.pscore / (1 - matching_df.pscore)


# %%
data = data.merge(
    matching_df[["pscore", "ps_weight"]], how="left", left_index=True, right_index=True
)
data["first_implementers"] = np.where(data.doi_year == 2017, 1, 0)

# %% Check balance -- Looks great
mod = smf.ols("pre_avescore ~ 1 + first_implementers + pscore", data[data.year == 2017])
res = mod.fit()
print(res.summary())

# %% First year results
mod = smf.ols("math ~ 1 + first_implementers + pscore", data[data.year == 2017])
res = mod.fit()
print(res.summary())

# %% Second year results
mod = smf.ols("math ~ 1 + first_implementers + pscore", data[data.year == 2018])
res = mod.fit()
print(res.summary())

# %% Third Year Results
mod = smf.ols("math ~ 1 + first_implementers + pscore", data[data.year == 2019])
res = mod.fit()
print(res.summary())

# %%
