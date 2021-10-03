#!/usr/bin/env python
# coding: utf-8

# %%

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from dofis import start
from dofis.analysis.library import analysis, regulations, tables

# %%

data = pd.read_csv(
    os.path.join(start.DATA_PATH, "clean", "master_data_district.csv"), sep=","
)
data = data.loc[(data.doi == 1)]
data = data[data.year == 2016]
data.head(5)


# In[5]:


def create_count_urban_df(data, list_of_regs, dict_of_reg_labels):
    n_col = []
    p_urban = []
    p_suburb = []
    p_town = []
    p_rural = []
    reg_labels = []
    f_p = []

    for reg in list_of_regs:
        n_col.append((len(data[data[reg] == 1])))
        p_urban.append(round(data[data.type_urban == 1][reg].mean(), 2))
        p_suburb.append(round(data[data.type_suburban == 1][reg].mean(), 2))
        p_town.append(round(data[data.type_town == 1][reg].mean(), 2))
        p_rural.append(round(data[data.type_rural == 1][reg].mean(), 2))
        reg_labels.append(dict_of_reg_labels[reg])
        formula = reg + "~ type_urban + type_suburban + type_town + type_rural - 1"
        df = data.dropna(
            subset=["type_urban", "type_suburban", "type_town", "type_rural", reg]
        )
        results = smf.ols(formula, data=df).fit()
        f_p.append(results.f_pvalue.round(2))

    df = pd.DataFrame(
        {
            "Regulation": reg_labels,
            "Count": n_col,
            "Urban": p_urban,
            "Suburban": p_suburb,
            "Town": p_town,
            "Rural": p_rural,
            "F-test p-value": f_p,
        }
    )

    return df


def create_count_proportion_df(data, var, list_of_regs, formula):
    n_col = []
    p_25 = []
    p_50 = []
    p_75 = []
    p_100 = []
    reg_labels = []
    f_p = []

    for reg in list_of_regs:
        n_col.append((len(data[data[reg] == 1])))
        for p_list, p in zip([p_25, p_50, p_75, p_100], [0.25, 0.5, 0.75, 1]):
            num = str(int(p * 100))
            p_var = var + num
            p_list.append(round(data[data[p_var] == 1][reg].mean(), 2))
        reg_labels.append(regulations.labels[reg])
        df = data.dropna(subset=[var, reg])
        full_formula = reg + formula
        results = smf.ols(full_formula, data=df).fit()
        f_p.append(results.f_pvalue.round(2))

    df = pd.DataFrame(
        {
            "Regulation": reg_labels,
            "Count": n_col,
            "Q1": p_25,
            "Q2": p_50,
            "Q3": p_75,
            "Q4": p_100,
            "F-test p-value": f_p,
        }
    )
    return df


# %% Urbancity

file_name = "desc_exemptionsXurbanicity.xlsx"
columns = ["Count", "Urban", "Suburban", "Town", "Rural", "F-test p-value"]

schedules_df = create_count_urban_df(data, regulations.schedules, regulations.labels)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=schedules_df,
    df_columns=columns,
    start_row=5,
    start_col=3,
)

class_size_df = create_count_urban_df(data, regulations.class_size, regulations.labels)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=class_size_df,
    df_columns=columns,
    start_row=10,
    start_col=3,
)

certification_df = create_count_urban_df(
    data, regulations.certification, regulations.labels
)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=certification_df,
    df_columns=columns,
    start_row=14,
    start_col=3,
)

contracts_df = create_count_urban_df(data, regulations.contracts, regulations.labels)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=contracts_df,
    df_columns=columns,
    start_row=18,
    start_col=3,
)

behavior_df = create_count_urban_df(data, regulations.behavior, regulations.labels)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=behavior_df,
    df_columns=columns,
    start_row=23,
    start_col=3,
)


# %% Teacher Turnaround

file_name = "desc_exemptionsXturnover.xlsx"
columns = ["Count", "Q1", "Q2", "Q3", "Q4", "F-test p-value"]
formula = " ~ pre_turnover25 + pre_turnover50 + pre_turnover75 + pre_turnover100"

schedules_df = create_count_proportion_df(
    data, "pre_turnover", regulations.schedules, formula
)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=schedules_df,
    df_columns=columns,
    start_row=5,
    start_col=3,
)

class_size_df = create_count_proportion_df(
    data, "pre_turnover", regulations.class_size, formula
)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=class_size_df,
    df_columns=columns,
    start_row=10,
    start_col=3,
)

certification_df = create_count_proportion_df(
    data, "pre_turnover", regulations.certification, formula
)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=certification_df,
    df_columns=columns,
    start_row=14,
    start_col=3,
)

contracts_df = create_count_proportion_df(
    data, "pre_turnover", regulations.contracts, formula
)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=contracts_df,
    df_columns=columns,
    start_row=18,
    start_col=3,
)

behavior_df = create_count_proportion_df(
    data, "pre_turnover", regulations.behavior, formula
)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=behavior_df,
    df_columns=columns,
    start_row=23,
    start_col=3,
)


# %% Prior Achievement


columns = ["Count", "Q1", "Q2", "Q3", "Q4", "F-test p-value"]
formula = " ~ pre_avescore25 + pre_avescore50 + pre_avescore75 + pre_avescore100"
file_name = "desc_exemptionsXachievement.xlsx"
schedules_df = create_count_proportion_df(
    data, "pre_avescore", regulations.schedules, formula
)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=schedules_df,
    df_columns=columns,
    start_row=5,
    start_col=3,
)

class_size_df = create_count_proportion_df(
    data, "pre_avescore", regulations.class_size, formula
)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=class_size_df,
    df_columns=columns,
    start_row=10,
    start_col=3,
)

certification_df = create_count_proportion_df(
    data, "pre_avescore", regulations.certification, formula
)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=certification_df,
    df_columns=columns,
    start_row=14,
    start_col=3,
)

contracts_df = create_count_proportion_df(
    data, "pre_avescore", regulations.contracts, formula
)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=contracts_df,
    df_columns=columns,
    start_row=18,
    start_col=3,
)

behavior_df = create_count_proportion_df(
    data, "pre_avescore", regulations.behavior, formula
)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=behavior_df,
    df_columns=columns,
    start_row=23,
    start_col=3,
)


# # Percent Hispanic

# In[19]:


columns = ["Count", "Q1", "Q2", "Q3", "Q4", "F-test p-value"]
formula = " ~ pre_hisp25 + pre_hisp50 + pre_hisp75 + pre_hisp100"
file_name = "desc_exemptionsXhispanic.xlsx"
schedules_df = create_count_proportion_df(
    data, "pre_hisp", regulations.schedules, formula
)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=schedules_df,
    df_columns=columns,
    start_row=5,
    start_col=3,
)

class_size_df = create_count_proportion_df(
    data, "pre_hisp", regulations.class_size, formula
)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=class_size_df,
    df_columns=columns,
    start_row=10,
    start_col=3,
)

certification_df = create_count_proportion_df(
    data, "pre_hisp", regulations.certification, formula
)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=certification_df,
    df_columns=columns,
    start_row=14,
    start_col=3,
)

contracts_df = create_count_proportion_df(
    data, "pre_hisp", regulations.contracts, formula
)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=contracts_df,
    df_columns=columns,
    start_row=18,
    start_col=3,
)

behavior_df = create_count_proportion_df(
    data, "pre_hisp", regulations.behavior, formula
)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=behavior_df,
    df_columns=columns,
    start_row=23,
    start_col=3,
)


# # Percent Black

# In[20]:


columns = ["Count", "Q1", "Q2", "Q3", "Q4", "F-test p-value"]
formula = " ~ pre_black25 + pre_black50 + pre_black75 + pre_hisp100"
file_name = "desc_exemptionsXblack.xlsx"
schedules_df = create_count_proportion_df(
    data, "pre_hisp", regulations.schedules, formula
)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=schedules_df,
    df_columns=columns,
    start_row=5,
    start_col=3,
)

class_size_df = create_count_proportion_df(
    data, "pre_hisp", regulations.class_size, formula
)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=class_size_df,
    df_columns=columns,
    start_row=10,
    start_col=3,
)

certification_df = create_count_proportion_df(
    data, "pre_hisp", regulations.certification, formula
)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=certification_df,
    df_columns=columns,
    start_row=14,
    start_col=3,
)

contracts_df = create_count_proportion_df(
    data, "pre_hisp", regulations.contracts, formula
)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=contracts_df,
    df_columns=columns,
    start_row=18,
    start_col=3,
)

behavior_df = create_count_proportion_df(
    data, "pre_hisp", regulations.behavior, formula
)
tables.df_to_excel(
    file=start.TABLE_PATH + file_name,
    df=behavior_df,
    df_columns=columns,
    start_row=23,
    start_col=3,
)
