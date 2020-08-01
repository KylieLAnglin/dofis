# %%
import pandas as pd
import numpy as np
import os
import sys
from linearmodels import PanelOLS

sys.path.append("../")
from library import start, analysis

# %%
data_path = start.data_path
table_path = start.table_path
data = pd.read_csv(os.path.join(data_path, 'clean', 'gdid_subject.csv'),
                   sep=",", low_memory=False)
data = data[data.doi]
print(data[(data.doi)].district.nunique())
print(data.doi_year.value_counts())
data.sample(5)


# %%
df = data.reset_index()
df['year'] = pd.to_datetime(df['year'], format='%Y')
# add column year to index
df = data.set_index(['year', 'campus'])
# swap indexes
df.index = df.index.swaplevel(0, 1)
df[['district', 'doi_year', 'treatpost']].sample(5)


# %%

df = analysis.create_interactions('total', df)

# %%
# GDID
mod = PanelOLS.from_formula(analysis.create_gdid_model_w_interactions(
    'total'),
    df[df.math == 1])
res = mod.fit(cov_type='clustered',
              clusters=df[df.math == 1].district)
print(res)
# %%
# GDID
mod = PanelOLS.from_formula(analysis.create_gdid_model_w_interactions(
    'total_log'),
    df[df.math == 1])
res = mod.fit(cov_type='clustered',
              clusters=df[df.math == 1].district)
print(res)

# %%
mod = PanelOLS.from_formula(analysis.create_linear_model_w_interactions(
    'total'),
    df[df.math == 1])
res = mod.fit(cov_type='clustered',
              clusters=df[df.math == 1].district)
print(res)


# %%
df = analysis.create_interactions('exempt_classsize', df)

mod = PanelOLS.from_formula(analysis.create_event_model_w_interactions(
    'exempt_classsize'),
                            df[df.math == 1])
res = mod.fit(cov_type='clustered', clusters=df[df.math == 1].district)
print(res)


# %%
df = analysis.create_interactions('pre_hisp', df)

mod = PanelOLS.from_formula(analysis.create_linear_model_w_interactions(
    'pre_hisp'),
                            df[df.math == 1])
res = mod.fit(cov_type='clustered', clusters=df[df.math == 1].district)
print(res)

# %%
