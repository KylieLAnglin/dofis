# %% Event Study Graphs - Math
# %%
# %%
import pandas as pd
import numpy as np
import pandas as pd
from openpyxl import load_workbook
import scipy
import matplotlib.pyplot as plt

from dofis import start
from dofis.analysis.library import analysis

MATH_AGG = start.TABLE_PATH + "results_math_ag_raw.xlsx"
math_agg = pd.read_excel(MATH_AGG)

MATH_DISAG = start.TABLE_PATH + "results_math_disag_raw.xlsx"
math_disag = pd.read_excel(MATH_DISAG)

READING_AGG = start.TABLE_PATH + "results_reading_ag_raw.xlsx"
reading_agg = pd.read_excel(READING_AGG)

READING_DISAG = start.TABLE_PATH + "results_reading_disag_raw.xlsx"
reading_disag = pd.read_excel(READING_DISAG)

data = pd.read_csv(start.DATA_PATH + "clean/r_data_school_2020_comparison.csv")
n = data.district.nunique()

# %%
# %%
coefs = []
ses = []
for row in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
    coef = math_agg.loc[row]["agg.dynamic.math.att.egt"]
    se = math_agg.loc[row]["agg.dynamic.math.se.egt"]
    coefs.append(coef)
    ses.append(se)


coef_df = pd.DataFrame(
    {
        "coef": coefs,
        "err": ses,
        "year": [-6, -5, -4, -3, -2, -1, 1, 2, 3],
    }
)
coef_df["lb"] = coef_df.coef - (1.96 * coef_df.err)
coef_df["ub"] = coef_df.coef + (1.96 * coef_df.err)
coef_df["errsig"] = coef_df.err * 1.96

fig, ax = plt.subplots(figsize=(8, 5))

coef_df.plot(
    x="year", y="coef", kind="bar", ax=ax, color="none", yerr="errsig", legend=False
)
ax.set_ylabel("")
ax.set_xlabel("")
ax.scatter(
    x=pd.np.arange(coef_df.shape[0]),
    marker="s",
    s=120,
    y=coef_df["coef"],
    color="black",
)
ax.axhline(y=0, linestyle="--", color="black", linewidth=4)
ax.xaxis.set_ticks_position("none")
_ = ax.set_xticklabels(
    ["Pre6", "Pre5", "Pre4", "Pre3", "Pre2", "Pre1", "Post1", "Post2", "Post3"],
    rotation=0,
)
# ax.set_title('Impact on Student Achievement - Event Study Coefficients',
# fontsize = 16)

# fig.savefig(start.table_path + "math_event_study" + ".png", bbox_inches="tight")

# %%
