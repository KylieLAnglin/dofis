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

from dofis.analysis.library import start
from dofis.analysis.library import analysis


# %%

data = pd.read_csv(
    os.path.join(start.data_path, "clean", "gdid_subject.csv"),
    sep=",",
    low_memory=False,
)
data = data[(data.doi)]
data = data[(data.doi != 2017)]

data.sample()

# %%

# convert year to datetime
df = data.reset_index()
df["year"] = pd.to_datetime(df["year"], format="%Y")
# add column year to index
df = data.set_index(["year", "campus"])
# swap indexes
df.index = df.index.swaplevel(0, 1)
df[["district", "doi_year", "treatpost"]].sample(5)

# %% Get table ready

gdid_model = "score_std ~ + 1 + treatpost + C(test_by_year) + EntityEffects"
linear_gdid_model = (
    "score_std ~ + 1 + treatpost + yearpost + "
    "yearpre  + C(test_by_year) + EntityEffects"
)
event_study_model = (
    "score_std ~ + 1 + pre5 + pre4 + pre3 + pre2 + "
    "post1 + post2 + + C(test_by_year) + EntityEffects"
)


mod = PanelOLS.from_formula(gdid_model, df)
res = mod.fit(cov_type="clustered", clusters=df.district)
print(res.summary)

mod = PanelOLS.from_formula(linear_gdid_model, df)
res = mod.fit(cov_type="clustered", clusters=df.district)
print(res.summary)


mod = PanelOLS.from_formula(event_study_model, df)
res = mod.fit(cov_type="clustered", clusters=df.district)
print(res.summary)
