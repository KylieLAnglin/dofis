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


def print_results_for_group(results: dict, group: int, col: int, start_row: int):
    col = col
    row = start_row

    for year in range(2013, 2020):
        te = results[group][year].params["treat_post"]
        pvalue = results[group][year].pvalues["treat_post"]
        ws.cell(row=row, column=col).value = analysis.coef_with_stars(
            te, pvalue=pvalue, n_tests=1, digits=2
        )
        row = row + 1
        se = results[group][year].bse["treat_post"]
        ws.cell(row=row, column=col).value = analysis.format_se(se, 2)
        row = row + 1
        wb.save(file_path)


# %% Math
math_results = analysis.dids(
    outcome="math_yr15std",
    group_var="group",
    time_var="year",
    cluster_var="district",
    df=data,
)

file_path = start.table_path + "results_math_all_groups_and_times.xlsx"
wb = load_workbook(file_path)
ws = wb.active

print_results_for_group(results=math_results, group=2017, col=2, start_row=3)
print_results_for_group(results=math_results, group=2018, col=3, start_row=3)
print_results_for_group(results=math_results, group=2019, col=4, start_row=3)

wb.save(file_path)


# %% Reading
reading_results = analysis.dids(
    outcome="reading_yr15std",
    group_var="group",
    time_var="year",
    cluster_var="district",
    df=data,
)

file_path = start.table_path + "results_reading_all_groups_and_times.xlsx"
wb = load_workbook(file_path)
ws = wb.active

print_results_for_group(results=reading_results, group=2017, col=2, start_row=3)
print_results_for_group(results=reading_results, group=2018, col=3, start_row=3)
print_results_for_group(results=reading_results, group=2019, col=4, start_row=3)

wb.save(file_path)

# %%
