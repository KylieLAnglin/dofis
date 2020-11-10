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
data = pd.read_csv(os.path.join(start.data_path, 'clean', 'gdid_subject.csv'),
                   sep=",", low_memory=False)
data = data[(data.doi)]


# convert year to datetime
df = data.reset_index()
df['year'] = pd.to_datetime(df['year'], format='%Y')
# add column year to index
df = data.set_index(['year', 'campus'])
# swap indexes
df.index = df.index.swaplevel(0, 1)
df[['district', 'doi_year', 'treatpost']].sample(5)
# %% Interaction Terms
df['group1'] = np.where(df.doi_year == 2017, 1, 0)
df['group2'] = np.where(df.doi_year == 2018, 1, 0)
df['group3'] = np.where(df.doi_year == 2019, 1, 0)

df['post1group1'] = np.where((df.doi_year == 2017) & (df.post1 == 1), 1, 0)
df['post1group2'] = np.where((df.doi_year == 2018) & (df.post1 == 1), 1, 0)
df['post1group3'] = np.where((df.doi_year == 2019) & (df.post1 == 1), 1, 0)

df['post2group1'] = np.where((df.doi_year == 2017) & (df.post2 == 1), 1, 0)
df['post2group2'] = np.where((df.doi_year == 2018) & (df.post2 == 1), 1, 0)

event_study_model = 'score_std ~ + 1 + pre5 + pre4 + pre3 + pre2 + ' \
    'post1 + post1group2 +  post1group3 + post2 + post2group1 + post3 \
         + C(test_by_year) + EntityEffects'
# %%

mod = PanelOLS.from_formula(event_study_model, df[df.math == 1])
res = mod.fit(cov_type='clustered', clusters=df[df.math == 1].district)
print(res)
# %%
