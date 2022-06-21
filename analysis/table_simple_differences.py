# %%

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import scipy
from openpyxl import load_workbook


from dofis.analysis.library import analysis, characteristics, regulations, tables
from dofis import start

# %%
df = pd.read_csv(start.DATA_PATH + "clean/master_data_school.csv")

# %%

# %%
FILE = start.TABLE_PATH + "Simple Pre-post Differences.xlsx"
wb = load_workbook(FILE)
ws = wb.active

# %%
GROUPS_FOR_TABLE = ["2017", "2018", "2019", "2020+", "Opt-out"]

OUTCOME = "teachers_uncertified"
row = 3
col = 2
for group in GROUPS_FOR_TABLE:
    col = 2
    for year in [2016, 2017, 2018, 2019, 2020, 2021]:
        value = df[(df.group == group) & (df.year == year)].teachers_uncertified.mean()
        ws.cell(row=row, column=col).value = round(value, 3)
        col = col + 1
        print(value)
    row = row + 1

wb.save(FILE)
