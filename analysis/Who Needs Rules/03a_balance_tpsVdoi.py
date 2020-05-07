#!/usr/bin/env python
# coding: utf-8

# %%

import os
import sys

import pandas as pd
import statsmodels.formula.api as sm
sys.path.append("../")
from library import analysis, characteristics, regulations, start, tables


# %%

data_path = start.data_path
table_path = start.table_path
data = pd.read_csv(os.path.join(start.data_path, 'clean',
                                'master_data_district.csv'),
                   sep=",", low_memory=False)
data = data.loc[(data['year'] == 2016) & (data['distischarter'] == 0)]
data = data.loc[(data['eligible19'] != 0) | (data['doi'] == True)]
print("Number of DOIS: ", len(data.loc[data.doi]))
print("Number of Eligible Non-DOIs", len(data.loc[~data.doi]))

# %% District Characteristics

district = analysis.many_y_one_x(data=data,
                                 y_list=characteristics.geography,
                                 y_labels=characteristics.labels,
                                 x='doi')
district


# %% Teacher Characteristics

teacher = analysis.many_y_one_x(data=data,
                                y_list=characteristics.teacher,
                                y_labels=characteristics.labels,
                                x='doi')
teacher


# %% Student Characteristics


student = analysis.many_y_one_x(data=data,
                                y_list=characteristics.student,
                                y_labels=characteristics.labels,
                                x='doi')
student

#
# ## To table

# %% To table


dfs = [district, teacher, student]
rows = [4, 13, 22]
tables.n_to_excel(file=table_path + 'balance_tpsVdoi.xlsx',
                  col=2, row=3, n=len(data[(data.doi)]))
tables.n_to_excel(file=table_path + 'balance_tpsVdoi.xlsx',
                  col=3, row=3, n=len(data[~data.doi]))
for df, row in zip(dfs, rows):
    tables.var_diff_to_excel(file=table_path + 'balance_tpsVdoi.xlsx',
                             df=df,
                             control_col='Control',
                             diff_col='Difference',
                             se_col='Std. Error', pvalue_col='P-value',
                             start_col=2, start_row=row)


# %%
