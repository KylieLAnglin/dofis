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


black_agg = pd.read_excel(start.TABLE_PATH + "results_black_ag_raw.xlsx")
hisp_agg = pd.read_excel(start.TABLE_PATH + "results_hisp_ag_raw.xlsx")
frpl_agg = pd.read_excel(start.TABLE_PATH + "results_frpl_ag_raw.xlsx")
iep_agg = pd.read_excel(start.TABLE_PATH + "results_iep_ag_raw.xlsx")
enrollment_agg = pd.read_excel(start.TABLE_PATH + "results_enrollment_ag_raw.xlsx")

data = pd.read_csv(start.DATA_PATH + "clean/r_data_school_2020_comparison.csv")
n = data.district.nunique()

# %%
# %%
def coef_df(df: pd.DataFrame):
    coefs = []
    ses = []
    for row in [0, 1, 2, 3, 4, 5, 6, 7]:
        coef = df.loc[row][3]
        se = df.loc[row][4]
        coefs.append(coef)
        ses.append(se)

    coef_df = pd.DataFrame(
        {
            "coef": coefs,
            "err": ses,
            "year": [-5, -4, -3, -2, -1, 1, 2, 3],
        }
    )
    coef_df["lb"] = coef_df.coef - (1.96 * coef_df.err)
    coef_df["ub"] = coef_df.coef + (1.96 * coef_df.err)
    coef_df["errsig"] = coef_df.err * 1.96
    return coef_df


# %%
black_df = coef_df(black_agg)
hisp_df = coef_df(hisp_agg)
frpl_df = coef_df(frpl_agg)
iep_df = coef_df(iep_agg)


fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
colors = ["gray", "gray", "gray", "gray", "gray", "black", "black", "black"]

ax1.scatter(
    x=pd.np.arange(black_df.shape[0]),
    marker="s",
    s=120,
    y=black_df["coef"],
    color=colors,
)
for pos, y, err, color in zip(
    pd.np.arange(black_df.shape[0]), black_df["coef"], black_df["errsig"], colors
):

    ax1.errorbar(pos, y, err, lw=2, capsize=4, capthick=4, color=color)

ax1.axhline(y=0, linestyle="--", color="black", linewidth=1)
ax1.xaxis.set_ticks_position("none")
_ = ax1.set_xticklabels(
    ["Pre5", "Pre4", "Pre3", "Pre2", "Pre1", "Post1", "Post2", "Post3"],
    rotation=0,
)
ax1.set_ylabel("Effect on Proportion Students")
ax1.set_title("Black")
ax1.set_ylim((-0.2, 0.2))

ax2.scatter(
    x=pd.np.arange(hisp_df.shape[0]),
    marker="s",
    s=120,
    y=hisp_df["coef"],
    color=colors,
)
for pos, y, err, color in zip(
    pd.np.arange(hisp_df.shape[0]), hisp_df["coef"], hisp_df["errsig"], colors
):

    ax2.errorbar(pos, y, err, lw=2, capsize=4, capthick=4, color=color)

ax2.axhline(y=0, linestyle="--", color="black", linewidth=1)
ax2.xaxis.set_ticks_position("none")
_ = ax2.set_xticklabels(
    ["Pre5", "Pre4", "Pre3", "Pre2", "Pre1", "Post1", "Post2", "Post3"],
    rotation=0,
)
ax2.set_ylabel("Effect on Proportion Students")
ax2.set_title("Hispanic")
ax2.set_ylim((-0.2, 0.2))


ax3.scatter(
    x=pd.np.arange(frpl_df.shape[0]),
    marker="s",
    s=120,
    y=frpl_df["coef"],
    color=colors,
)
for pos, y, err, color in zip(
    pd.np.arange(frpl_df.shape[0]), frpl_df["coef"], frpl_df["errsig"], colors
):

    ax3.errorbar(pos, y, err, lw=2, capsize=4, capthick=4, color=color)

ax3.axhline(y=0, linestyle="--", color="black", linewidth=1)
ax3.xaxis.set_ticks_position("none")
_ = ax3.set_xticklabels(
    ["Pre5", "Pre4", "Pre3", "Pre2", "Pre1", "Post1", "Post2", "Post3"],
    rotation=0,
)
ax3.set_ylabel("Effect on Proportion Students")
ax3.set_title("Free/Reduced Price Lunch")
ax3.set_ylim((-0.1, 0.1))

ax4.scatter(
    x=pd.np.arange(iep_df.shape[0]),
    marker="s",
    s=120,
    y=iep_df["coef"],
    color=colors,
)
for pos, y, err, color in zip(
    pd.np.arange(iep_df.shape[0]), iep_df["coef"], iep_df["errsig"], colors
):

    ax4.errorbar(pos, y, err, lw=2, capsize=4, capthick=4, color=color)

ax4.axhline(y=0, linestyle="--", color="black", linewidth=1)
ax4.xaxis.set_ticks_position("none")
_ = ax4.set_xticklabels(
    ["Pre5", "Pre4", "Pre3", "Pre2", "Pre1", "Post1", "Post2", "Post3"],
    rotation=0,
)
ax4.set_ylabel("Effect on Proportion Students")
ax4.set_title("Individualized Education Plan")
ax4.set_ylim((-5, 5))


fig.savefig(
    start.TABLE_PATH + "enrollment_results_event_study" + ".png", bbox_inches="tight"
)
