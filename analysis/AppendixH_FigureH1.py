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


days_agg = pd.read_excel(start.TABLE_PATH + "results_days_ag_raw_average.xlsx")
before_agg = pd.read_excel(
    start.TABLE_PATH + "results_days_before_first_week_ag_raw_average.xlsx"
)

data = pd.read_csv(start.DATA_PATH + "clean/r_data.csv")
n = data.district.nunique()

# %%
# %%
def coef_df(df: pd.DataFrame):
    coefs = []
    ses = []
    for year in df["agg.dynamic.egt"]:
        coef = df.loc[df["agg.dynamic.egt"] == year, "agg.dynamic.att.egt"]
        se = df.loc[df["agg.dynamic.egt"] == year, "agg.dynamic.se.egt"]
        coefs.append(coef)
        ses.append(se)

    coef_df = pd.DataFrame(
        {
            "coef": coefs,
            "err": ses,
            "year": list(df["agg.dynamic.egt"]),
        }
    )
    coef_df["lb"] = coef_df.coef - (1.96 * coef_df.err)
    coef_df["ub"] = coef_df.coef + (1.96 * coef_df.err)
    coef_df["errsig"] = coef_df.err * 1.96
    return coef_df


# %%

days_df = coef_df(days_agg)
before_df = coef_df(before_agg)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 10))

colors = [
    "gray",
    "black",
    "black",
]

# days
ax1.scatter(
    x=days_df.year,
    marker="s",
    s=120,
    y=days_df["coef"],
    color=colors,
)
for pos, y, err, color in zip(days_df.year, days_df["coef"], days_df["errsig"], colors):

    ax1.errorbar(pos, y, err, lw=2, capsize=4, capthick=4, color=color)

ax1.axhline(y=0, linestyle="--", color="black", linewidth=1)
ax1.set_xticks(days_df.year)
ax1.set_yticks([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])

ax1.set_ylabel("Days")
ax1.set_title("Number of Instruction Days")
ax1.set_ylim((-5, 5))


# Days before third week
ax2.scatter(
    x=days_df.year,
    marker="s",
    s=120,
    y=before_df["coef"],
    color=colors,
)
for pos, y, err, color in zip(
    before_df.year, before_df["coef"], before_df["errsig"], colors
):

    ax2.errorbar(pos, y, err, lw=2, capsize=4, capthick=4, color=color)

ax2.axhline(y=0, linestyle="--", color="black", linewidth=1)
ax2.set_xticks(before_df.year)
ax2.set_yticks([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])


ax2.set_ylabel("Days")
ax2.set_title("Number of Instruction Days before Third Week of August")
ax2.set_ylim((-5, 5))


fig.savefig(start.TABLE_PATH + "AppendixH" + ".png", bbox_inches="tight")
