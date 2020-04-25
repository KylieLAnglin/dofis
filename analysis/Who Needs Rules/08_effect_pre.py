#!/usr/bin/env python
# coding: utf-8

# In[1]:

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
from library import (analysis, characteristics, print_statistics, regulations,
                     start, tables)


# %%

data_path = start.data_path
table_path = start.table_path
data = pd.read_csv(os.path.join(data_path, 'clean', 'gdid_school.csv'),
                   sep=",", low_memory=False)
data = data[(data.doi)]
print(data[(data.doi)].district.nunique())
data.sample()


# %%

subjects = ['m_3rd_avescore', 'm_4th_avescore',  'm_5th_avescore',
            'm_6th_avescore', 'm_7th_avescore', 'm_8th_avescore',
            'alg_avescore',
            'r_3rd_avescore', 'r_4th_avescore', 'r_5th_avescore',
            'r_6th_avescore', 'r_7th_avescore', 'r_8th_avescore',
            'eng1_avescore',  'bio_avescore']
math_tests = ['m_3rd_avescore', 'm_4th_avescore', 'm_5th_avescore',
              'm_6th_avescore', 'm_7th_avescore', 'm_8th_avescore',
              'alg_avescore']
reading_tests = ['r_3rd_avescore', 'r_4th_avescore', 'r_5th_avescore',
                 'r_6th_avescore', 'r_7th_avescore', 'r_8th_avescore',
                 'eng1_avescore']


# In[6]:


# convert year to datetime
df = data.reset_index()
df['year'] = pd.to_datetime(df['year'], format='%Y')
# add column year to index
df = df.set_index(['campus', 'year'])
# swap indexes
df.index = df.index.swaplevel(0, 1)
df[['district', 'doi_year', 'treatpost', 'pre1']].sample(5, random_state=8)


# In[7]:


def many_y_one_x_controls(data, y_list, y_labels, x):
    regs = []
    cons = []
    coef = []
    se = []
    pvalue = []

    for y in y_list:
        df = data.replace(np.inf, np.nan)
        df = df.replace(-np.inf, np.nan).dropna(subset=[y])
        formula = y + ' ~ + 1 + pre1 + EntityEffects'
        print(formula)
        mod = PanelOLS.from_formula(formula, df)
        # result = mod.fit()
        result = mod.fit(cov_type='clustered',
                         cluster_entity=True,
                         cluster_time=True)
        # result = mod.fit(cov_type='clustered', clusters = data.district)

        cons.append(result.params["Intercept"].round(2))
        if str(data[x].dtypes) == 'bool':
            var = x + '[T.True]'
        else:
            var = x
        coef.append(result.params[var].round(2))
        se.append(result.std_errors[var].round(2))
        pvalue.append(result.pvalues[var].round(2))
        regs.append(y_labels[y])

    df = pd.DataFrame(
        {'Characteristic': regs,
         'Control': cons,
         'Difference': coef,
         'Std. Error': se,
         'P-value': pvalue,
         })
    return df


# In[8]:


district = many_y_one_x_controls(df, characteristics.geography,
                                 characteristics.labels, 'pre1')
district


# In[10]:


teachers = many_y_one_x_controls(df, characteristics.teacher,
                                 characteristics.labels, 'pre1')
teachers


# In[11]:


students = many_y_one_x_controls(df, characteristics.student,
                                 characteristics.labels, 'pre1')
students


# In[12]:


dfs = [district, teachers, students]
rows = [5, 14, 23]
for df, row in zip(dfs, rows):
    tables.var_diff_to_excel(file=table_path + 'balance_controls.xlsx',
                             df=df,
                             control_col='Control',
                             diff_col='Difference',
                             se_col='Std. Error', pvalue_col='P-value',
                             start_col=2, start_row=row)
