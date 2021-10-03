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
from linearmodels import PanelOLS
from openpyxl import load_workbook
from patsy import dmatrices

from dofis import start
from dofis.analysis.library import analysis


# %%

data = pd.read_csv(
    os.path.join(start.data_path, "clean", "master_data_district.csv"),
    sep=",",
    low_memory=False,
)

print(data[data.year == 2016].doi_year.value_counts())

data.sample()

# %%

# convert year to datetime
df = data.reset_index()
df["year_index"] = pd.to_datetime(df["year"], format="%Y")
df["district_index"] = df.district
df = df.set_index(["district_index", "year_index"])


df["doi_2017"] = np.where(df.doi_year == 2017, 1, 0)
df["doi_2018"] = np.where(df.doi_year == 2018, 1, 0)
df["doi_2019"] = np.where(df.doi_year == 2019, 1, 0)

df[
    [
        "year",
        "doi_year",
        "treatpost",
        "yearpost",
        "post1",
        "math",
        "reading",
        "elem_math",
        "doi_2017",
        "doi_2018",
        "doi_2019",
        "charter",
    ]
].sample(5)

df = df[(df.analytic_sample) | (df.charter)]

# %%
model_df = df[(df.doi_2017) | (df.charter)]
model_df["yr_centered"] = df.year - 2017
model_df["yr_centered"] = df.year - 2017

model_df["yearpost"] = np.where(
    model_df.year >= model_df.doi_year, model_df.year - model_df.doi_year, 0
)  # phase-in
model_df["yearpre"] = np.where(
    model_df.year <= model_df.doi_year, model_df.year - model_df.doi_year, 0
)  # pre-trend

model_df
CITS_MODEL = "~ + 1 + doi_2017 + yr_centered"
