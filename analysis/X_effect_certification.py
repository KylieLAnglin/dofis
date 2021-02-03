# %%

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from linearmodels import PanelOLS

from dofis.analysis.library import analysis
from dofis.analysis.library import regulations
from dofis.analysis.library import start

# %% School Data
data_school = pd.read_csv(
    os.path.join(start.data_path, "clean", "master_data_school.csv"),
    sep=",",
    low_memory=False,
)
data_school = data_school[data_school.doi]


df = pd.read_csv(
    os.path.join(start.data_path, "clean", "gdid_school.csv"), sep=",", low_memory=False
)
df = df[df.year.isin([2016, 2017, 2018, 2019])]
# df = data_school.copy()

# convert year to datetime
df = df.reset_index()
df["year"] = pd.to_datetime(df["year"], format="%Y")
# add column year to index
df = df.set_index(["year", "campus"])
# swap indexes
df.index = df.index.swaplevel(0, 1)

df["pre2"] = np.where((df.pre2 == 1) | (df.pre3 == 1), 1, 0)

EVENT_STUDY_MODEL = "~ + 1 + pre2 + post1 + post2 + post3 + EntityEffects + TimeEffects"
# %% Effect Certification

event_study_model = "teachers_certified" + EVENT_STUDY_MODEL

mod = PanelOLS.from_formula(event_study_model, data=df)
res = mod.fit(cov_type="clustered", clusters=df.district)
print(res)

# %% Effect Uncertified Teachers


mod = PanelOLS.from_formula("teachers_uncertified" + EVENT_STUDY_MODEL, data=df)
res = mod.fit(cov_type="clustered", clusters=df.district)
print(res)

# %% # %% Effect secondary math

mod = PanelOLS.from_formula(
    "teachers_secondary_math_teachers_with_cert" + EVENT_STUDY_MODEL, data=df
)
res = mod.fit(cov_type="clustered", clusters=df.district)
print(res)


# %% NUMBER of out of field secondary math teachers

mod = PanelOLS.from_formula(
    "outoffield_secondary_math_teacher" + EVENT_STUDY_MODEL, data=df
)
res = mod.fit(cov_type="clustered", clusters=df.district)
print(res)

# %%
mod = PanelOLS.from_formula(
    "outoffield_secondary_science_teacher" + EVENT_STUDY_MODEL, data=df
)
res = mod.fit(cov_type="clustered", clusters=df.district)
print(res)
# %%
