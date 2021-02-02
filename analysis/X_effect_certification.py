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
df = df[~df.teachers_secondary_math_teachers_with_cert.isnull()]
df = df[df.post3 == 0]

# convert year to datetime
df = df.reset_index()
df["year"] = pd.to_datetime(df["year"], format="%Y")
# add column year to index
df = df.set_index(["year", "campus"])
# swap indexes
df.index = df.index.swaplevel(0, 1)


event_study_model = (
    "teachers_secondary_math_teachers_with_cert ~ + 1 + pre5 + pre4 + pre3 + pre2 + "
    "post1 + post2 + EntityEffects + TimeEffects"
)

mod = PanelOLS.from_formula(event_study_model, data=df)
res = mod.fit(cov_type="clustered", clusters=df.district)
# %%
