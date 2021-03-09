#!/usr/bin/env python
# coding: utf-8

# %%
import os
import sys

import numpy as np
import pandas as pd
from openpyxl import load_workbook

from dofis.analysis.library import start
from dofis.analysis.library import analysis


# %%

data = pd.read_csv(
    os.path.join(start.data_path, "clean", "r_data_school_2020_comparison.csv"),
    sep=",",
    low_memory=False,
)

data.sample()

# %%
math_results = analysis.dids(
    outcome="math_yr15std",
    group_var="group",
    time_var="year",
    cluster_var="district",
    df=data,
)

# %%
