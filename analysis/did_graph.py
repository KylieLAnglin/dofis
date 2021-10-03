#!/usr/bin/env python
# coding: utf-8

# %%
import os
import sys
import random

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from linearmodels import PanelOLS
from openpyxl import load_workbook
from patsy import dmatrices

from dofis import start
from dofis.analysis.library import analysis


# %%

data = pd.read_csv(
    os.path.join(start.data_path, "clean", "r_data_school_2020_comparison.csv"),
    sep=",",
    low_memory=False,
)

data.sample()

# %%
def did(
    did_df: pd.DataFrame,
    outcome: str,
    treat_indicator: str,
    post_indicator: str,
    treat_post_indicator: str,
    cluster_var: str,
    quietly: bool = True,
):
    formula = (
        outcome
        + "~ 1 + "
        + treat_indicator
        + " + "
        + post_indicator
        + " + "
        + treat_post_indicator
    )

    mod = smf.ols(formula, did_df)
    res = mod.fit()
    res = mod.fit(cov_type="cluster", cov_kwds={"groups": did_df[cluster_var]})
    if not quietly:
        print(res.summary())

    return res


# %% 2017 implementers in 2017
data["pre_implementation"] = np.where(data.year < data.group, 1, 0)

# %%
implementation_group = 2017
year = 2017
df = data[(data.year == year) | (data.year == year - 1)]  # limit to two years
df = df[(data.group == implementation_group) | data.group < year]  # limit to two groups

df["treat"] = np.where(df.group == implementation_group, 1, 0)
df["post"] = np.where(df.year == year, 1, 0)
df["treat_post"] = df.treat * df.post

results = did(
    did_df=df,
    outcome="math_yr15std",
    treat_indicator="treat",
    post_indicator="post",
    treat_post_indicator="treat_post",
    cluster_var="district",
    quietly=False,
)

plt_df = (
    df[["treat", "year", "math_yr15std"]]
    .groupby(by=["treat", "year"])
    .mean()
    .reset_index()
)

comparison_change = (
    plt_df[(plt_df.treat == 0) & (plt_df.year == 2017)]["math_yr15std"].mean()
    - plt_df[(plt_df.treat == 0) & (plt_df.year == 2016)]["math_yr15std"].mean()
)

treatment_pre = plt_df[(plt_df.treat == 1) & (plt_df.year == 2016)][
    "math_yr15std"
].mean()
treatment_counterfactual = treatment_pre + comparison_change

counterfactual = plt_df[plt_df.treat == 1]
counterfactual["math_yr15std"] = np.where(
    counterfactual.year == 2017, treatment_counterfactual, counterfactual.math_yr15std
)

fig, ax = plt.subplots(1, 1)
# get_ipython().run_line_magic('matplotlib', 'inline')
plt.style.use("seaborn")
my_dpi = 96
plt.figure(figsize=(480 / my_dpi, 480 / my_dpi), dpi=my_dpi)


ax.plot(
    list(plt_df[plt_df.treat == 0].year),
    plt_df[plt_df.treat == 0]["math_yr15std"],
    label="2018, 2019, and 2020 Implementers",
    linestyle="-",
    color="gray",
)
ax.plot(
    list(plt_df[plt_df.treat == 0].year),
    plt_df[plt_df.treat == 1]["math_yr15std"],
    label="2017 Implementers",
    linestyle="-",
    color="black",
)

ax.plot(
    list(counterfactual[counterfactual.treat == 1].year),
    counterfactual[counterfactual.treat == 1]["math_yr15std"],
    label="2017 Counterfactual",
    linestyle="--",
    color="black",
)

ax.set_ylim(0, 0.6)
ax.set_xlim(2015.5, 2017.5)

ax.set_xticks([2016, 2017])

ax.set_xlabel("Year")
ax.set_ylabel("School-Level Standardized Mathematics Scores")

ax.legend()


# %%
implementation_group = 2017
year = 2019
df = data[
    (data.year == year) | (data.year == implementation_group - 1)
]  # limit to two years
df = df[
    (data.group == implementation_group) | (data.group > year) | (data.group == 0)
]  # limit to two groups

df["treat"] = np.where(df.group == implementation_group, 1, 0)
df["post"] = np.where(df.year == year, 1, 0)
df["treat_post"] = df.treat * df.post

results = did(
    did_df=df,
    outcome="math_yr15std",
    treat_indicator="treat",
    post_indicator="post",
    treat_post_indicator="treat_post",
    cluster_var="district",
    quietly=False,
)

plt_df = (
    df[["treat", "year", "math_yr15std"]]
    .groupby(by=["treat", "year"])
    .mean()
    .reset_index()
)

comparison_change = (
    plt_df[(plt_df.treat == 0) & (plt_df.year == 2019)]["math_yr15std"].mean()
    - plt_df[(plt_df.treat == 0) & (plt_df.year == 2016)]["math_yr15std"].mean()
)

treatment_pre = plt_df[(plt_df.treat == 1) & (plt_df.year == 2016)][
    "math_yr15std"
].mean()
treatment_counterfactual = treatment_pre + comparison_change

counterfactual = plt_df[plt_df.treat == 1]
counterfactual["math_yr15std"] = np.where(
    counterfactual.year == 2019, treatment_counterfactual, counterfactual.math_yr15std
)

fig, ax = plt.subplots(1, 1)
# get_ipython().run_line_magic('matplotlib', 'inline')
plt.style.use("seaborn")
my_dpi = 96
plt.figure(figsize=(480 / my_dpi, 480 / my_dpi), dpi=my_dpi)


ax.plot(
    list(plt_df[plt_df.treat == 0].year),
    plt_df[plt_df.treat == 0]["math_yr15std"],
    label="2020 Implementers",
    linestyle="-",
    color="gray",
)
ax.plot(
    list(plt_df[plt_df.treat == 0].year),
    plt_df[plt_df.treat == 1]["math_yr15std"],
    label="2017 Implementers",
    linestyle="-",
    color="black",
)

ax.plot(
    list(counterfactual[counterfactual.treat == 1].year),
    counterfactual[counterfactual.treat == 1]["math_yr15std"],
    label="2017 Counterfactual",
    linestyle="--",
    color="black",
)

ax.set_ylim(0, 1)
ax.set_xlim(2015.5, 2019.5)

ax.set_xticks([2016, 2017, 2018, 2019])

ax.set_xlabel("Year")
ax.set_ylabel("School-Level Standardized Mathematics Scores")

ax.legend()
# %%
