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

sys.path.append("../")
from library import analysis, print_statistics, start


# In[27]:


data = pd.read_csv(os.path.join(start.data_path, 'clean',
                                'master_data_district.csv'),
                   sep=",", low_memory=False)
data = data[(data.doi)]
print(data[(data.doi)].district.nunique())
print(data.district.nunique())


# %%

# convert year to datetime
df = data.reset_index()
df['year'] = pd.to_datetime(df['year'], format='%Y')
df = df.set_index(['year', 'district'])
df.index = df.index.swaplevel(0, 1)
df[['doi_year', 'treatpost', 'treatpost',
    'pre5', 'pre4', 'pre3', 'pre2', 'pre1',
    'post1', 'post2', 'post3']].sample(5, random_state=10)


# %% Specifications

gdid_model = 'school_spread ~ + 1 + treatpost + EntityEffects + TimeEffects'
linear_gdid_model = 'school_spread ~ + 1 + treatpost + yearpost + yearpre' \
    ' + EntityEffects + TimeEffects'
event_study_model = 'school_spread ~ + 1 + pre5 + pre4 + pre3 + pre2' \
    ' + post1 + post2 + post3 + + EntityEffects + TimeEffects'

# %% Event Study

mod = PanelOLS.from_formula(event_study_model, df)
res = mod.fit(cov_type='clustered', cluster_entity=True)
print(res)


# %% GDID


mod = PanelOLS.from_formula(gdid_model, df)
res = mod.fit(cov_type='clustered', cluster_entity=True)
print(res)

# %% Linear GDID

mod = PanelOLS.from_formula(linear_gdid_model, df)
res = mod.fit(cov_type='clustered', cluster_entity=True)
print(res)
