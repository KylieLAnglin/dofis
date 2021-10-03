# %%


import os
import sys

import numpy as np
import pandas as pd
import statsmodels.formula.api as sm

from dofis import start
from dofis.analysis.library import analysis
from dofis.analysis.library import tables
from dofis.analysis.library import characteristics


data = pd.read_csv(
    os.path.join(start.DATA_PATH, "clean", "master_data_school.csv"),
    sep=",",
    low_memory=False,
)
data = data[data.year == 2016]
data.doi_year.value_counts().sort_index()

# %%


data[["doi", "doi_year"]].sample(5)
col_names = ["texas", 2017, 2018, 2019, "tps"]


# %% Geography

data.type_description.value_counts()
data.geography.value_counts()
data.distischarter.value_counts()

labels = []
for char in characteristics.geography:
    labels.append(characteristics.labels[char])
    labels.append("")
table_dict = {"Characteristics": labels}
geo_table = pd.DataFrame(data=table_dict)

for yr in col_names:
    if yr == "texas":
        df = data[(data.distischarter == 0)]
    elif yr == "tps":
        df = data[(data.doi == 0) & (data.distischarter == 0)]
    else:
        df = data[data.doi_year == yr]
    means = []
    for char in characteristics.geography:
        means.append(round(df[char].mean(), 2))
        sd = "[" + str(round(df[char].std(), 2)) + "]"
        means.append(sd)
    geo_table[yr] = means

geo_table


# # Teacher characteristics

# %%


labels = []
for char in characteristics.teacher:
    labels.append(characteristics.labels[char])
    labels.append("")
table_dict = {"Characteristics": labels}
teacher_table = pd.DataFrame(data=table_dict)

for yr in col_names:
    means = []
    if yr == "texas":
        df = data[(data.distischarter == 0)]
    elif yr == "tps":
        df = data[(data.doi == 0) & (data.distischarter == 0)]
    else:
        df = data[data.doi_year == yr]
    for char in characteristics.teacher:
        means.append(round(df[char].mean(), 2))
        sd = "[" + str(round(df[char].std(), 2)) + "]"
        means.append(sd)
    teacher_table[yr] = means

teacher_table


# %% Student

labels = []
for char in characteristics.student:
    labels.append(characteristics.labels[char])
    labels.append("")
table_dict = {"Characteristics": labels}
student_table = pd.DataFrame(data=table_dict)

for yr in col_names:
    if yr == "texas":
        df = data[(data.distischarter == 0)]
    elif yr == "tps":
        df = data[(data.doi == 0) & (data.distischarter == 0)]
    else:
        df = data[data.doi_year == yr]
    means = []
    for char in characteristics.student:
        means.append(round(df[char].mean(), 2))
        sd = "[" + str(round(df[char].std(), 2)) + "]"
        means.append(sd)
    student_table[yr] = means

student_table


# %% To Table
table_file = "school_characteristics_by_year.xlsx"
dfs = [geo_table, teacher_table, student_table]
rows = [4, 13, 22]
for df, row in zip(dfs, rows):
    tables.df_to_excel(
        file=start.TABLE_PATH + table_file,
        df=df,
        df_columns=col_names,
        start_col=2,
        start_row=row,
    )


# %%

tables.n_to_excel(
    file=start.TABLE_PATH + table_file,
    col=2,
    row=33,
    n=len(data[data.distischarter == 0]),
)
tables.n_to_excel(
    file=start.TABLE_PATH + table_file,
    col=3,
    row=33,
    n=len(data[data.doi_year == col_names[1]]),
)
tables.n_to_excel(
    file=start.TABLE_PATH + table_file,
    col=4,
    row=33,
    n=len(data[data.doi_year == col_names[2]]),
)
tables.n_to_excel(
    file=start.TABLE_PATH + table_file,
    col=5,
    row=33,
    n=len(data[data.doi_year == col_names[3]]),
)
tables.n_to_excel(
    file=start.TABLE_PATH + table_file,
    col=6,
    row=33,
    n=len(data[(data.doi == 0) & (data.distischarter == 0)]),
)
