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
    os.path.join(start.data_path, "clean", "master_data_district.csv"),
    sep=",",
    low_memory=False,
)

print(data[data.year == 2016].doi_year.value_counts())

data.sample()

# %%
    mod = PanelOLS.from_formula(GDID_MODEL, data)
    res = mod.fit(cov_type="clustered", clusters=data.district)