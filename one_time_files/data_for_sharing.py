# %%
import os

import numpy as np
import pandas as pd

from dofis.merge_and_clean.library import clean_final
from dofis.merge_and_clean.library import clean_for_merge
from dofis import start

pd.options.display.max_columns = 200

df = pd.read_csv(start.DATA_PATH + "clean/master_data_district.csv")
df = df[df.year == 2019]

var_list = [
    "district",
    "distname",
    "doi",
    "distischarter",
    "link",
    "term_year",
    "term_month",
    "finalize_year",
    "finalize_month",
]

reg_vars = [c for c in df.columns if c.lower()[:3] == "reg"]
vars_to_keep = var_list + reg_vars

df = df[vars_to_keep]
df = df.drop(columns=["reg28_0216"])

df.to_csv(start.DATA_PATH + "clean/doi_status_and_exemptions.csv")
  