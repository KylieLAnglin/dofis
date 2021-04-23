# %%
import pandas as pd
import numpy as np
import pandas as pd
from openpyxl import load_workbook
import scipy

from dofis.analysis.library import start
from dofis.analysis.library import analysis

# %%
results_path = start.table_path + "/results_subjects_raw.xlsx"
results = pd.read_excel(results_path).set_index("outcome")


file_path = start.table_path + "results_subjects.xlsx"
wb = load_workbook(file_path)
ws = wb.active

col = 2
row = 5
for outcome in [
    "m_3rd_std",
    "m_4th_std",
    "m_5th_std",
    "m_6th_std",
    "m_7th_std",
    "m_8th_std",
    "alg_std",
]:
    te = results.loc[outcome, "te"]
    se = results.loc[outcome, "se"]
    pvalue = (
        scipy.stats.t.sf(np.abs(te / se), n - 1) * 2
    )  # two-sided pvalue = Prob(abs(t)>tt)

    ws.cell(row=row, column=col).value = analysis.coef_with_stars(
        te, pvalue=pvalue, n_tests=7, digits=2
    )
    row = row + 1
    ws.cell(row=row, column=col).value = analysis.format_se(se, 2)
    row = row + 1

col = 4
row = 5
for outcome in [
    "r_3rd_std",
    "r_4th_std",
    "r_5th_std",
    "r_6th_std",
    "r_7th_std",
    "r_8th_std",
    "eng1_std",
]:
    te = results.loc[outcome, "te"]
    se = results.loc[outcome, "se"]
    pvalue = (
        scipy.stats.t.sf(np.abs(te / se), n - 1) * 2
    )  # two-sided pvalue = Prob(abs(t)>tt)

    ws.cell(row=row, column=col).value = analysis.coef_with_stars(
        te, pvalue=pvalue, n_tests=7, digits=2
    )
    row = row + 1
    ws.cell(row=row, column=col).value = analysis.format_se(se, 2)
    row = row + 1

wb.save(file_path)