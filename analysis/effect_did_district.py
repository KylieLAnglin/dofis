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
    os.path.join(start.data_path, "clean", "r_data_district_charter_comparison.csv"),
    sep=",",
    low_memory=False,
)

data.sample()


# %%
did_df = data[
    ((data.group == 2017) | (data.group == 0))
    & ((data.year == 2017) | (data.year == 2016))
]

did_df["treat"] = np.where(did_df.doi == True, 1, 0)
did_df["post"] = np.where(did_df.year == 2017, 1, 0)
did_df["treat_post"] = did_df.treat * did_df.post


mod = smf.ols("elem_math ~ 1 + treat + post + treat_post", did_df)
res = mod.fit(cov_type="cluster", cov_kwds={"groups": did_df["district"]})
print(res.summary())
# %%
