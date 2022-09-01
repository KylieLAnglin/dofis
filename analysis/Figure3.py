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


uncertified_agg = pd.read_excel(start.TABLE_PATH + "results_uncertified_ag_raw.xlsx")
out_of_field_agg = pd.read_excel(start.TABLE_PATH + "results_out_of_field_ag_raw.xlsx")
class_size_agg = pd.read_excel(start.TABLE_PATH + "results_class_size_elem_ag_raw.xlsx")
ratio_agg = pd.read_excel(start.TABLE_PATH + "results_stu_teach_ratio_ag_raw.xlsx")
data = pd.read_csv(start.DATA_PATH + "clean/r_data.csv")
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

cert_df = coef_df(uncertified_agg)
classes_df = coef_df(class_size_agg)
ratio_df = coef_df(ratio_agg)
field_df = coef_df(out_of_field_agg)

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
colors = ["gray", "gray", "gray", "gray", "gray", "black", "black", "black"]

# Uncertified
ax1.scatter(
    x=pd.np.arange(cert_df.shape[0]),
    marker="s",
    s=120,
    y=cert_df["coef"],
    color=colors,
)
for pos, y, err, color in zip(
    pd.np.arange(cert_df.shape[0]), cert_df["coef"], cert_df["errsig"], colors
):

    ax1.errorbar(pos, y, err, lw=2, capsize=4, capthick=4, color=color)

ax1.axhline(y=0, linestyle="--", color="black", linewidth=1)
ax1.xaxis.set_ticks_position("none")
_ = ax1.set_xticklabels(
    ["Pre5", "Pre4", "Pre3", "Pre2", "Pre1", "Post1", "Post2", "Post3"],
    rotation=0,
)
ax1.set_ylabel("Proportion")
ax1.set_title("Proportion Uncertified Teachers")
ax1.set_ylim((-0.05, 0.05))

# Out of field
ax2.scatter(
    x=pd.np.arange(field_df.shape[0]),
    marker="s",
    s=120,
    y=field_df["coef"],
    color=colors,
)
for pos, y, err, color in zip(
    pd.np.arange(field_df.shape[0]), field_df["coef"], field_df["errsig"], colors
):

    ax2.errorbar(pos, y, err, lw=2, capsize=4, capthick=4, color=color)

ax2.axhline(y=0, linestyle="--", color="black", linewidth=1)
ax2.xaxis.set_ticks_position("none")
_ = ax2.set_xticklabels(
    ["Pre5", "Pre4", "Pre3", "Pre2", "Pre1", "Post1", "Post2", "Post3"],
    rotation=0,
)
ax2.set_ylabel("Effect Size Estimate")
ax2.set_title("Percent Out-of-field Teachers")
ax2.set_ylim((-0.1, 0.1))

# Class Size
ax3.scatter(
    x=pd.np.arange(cert_df.shape[0]),
    marker="s",
    s=120,
    y=classes_df["coef"],
    color=colors,
)
for pos, y, err, color in zip(
    pd.np.arange(classes_df.shape[0]), classes_df["coef"], classes_df["errsig"], colors
):

    ax3.errorbar(pos, y, err, lw=2, capsize=4, capthick=4, color=color)

ax3.axhline(y=0, linestyle="--", color="black", linewidth=1)
ax3.xaxis.set_ticks_position("none")
_ = ax3.set_xticklabels(
    ["Pre5", "Pre4", "Pre3", "Pre2", "Pre1", "Post1", "Post2", "Post3"],
    rotation=0,
)
ax3.set_ylabel("Students")
ax3.set_title("Effect on Average Class Size")
ax3.set_ylim((-3, 3))

# Student-Teacher Ratio
ax4.scatter(
    x=pd.np.arange(ratio_df.shape[0]),
    marker="s",
    s=120,
    y=ratio_df["coef"],
    color=colors,
)
for pos, y, err, color in zip(
    pd.np.arange(ratio_df.shape[0]), ratio_df["coef"], ratio_df["errsig"], colors
):

    ax4.errorbar(pos, y, err, lw=2, capsize=4, capthick=4, color=color)

ax4.axhline(y=0, linestyle="--", color="black", linewidth=1)
ax4.xaxis.set_ticks_position("none")
_ = ax4.set_xticklabels(
    ["Pre5", "Pre4", "Pre3", "Pre2", "Pre1", "Post1", "Post2", "Post3"],
    rotation=0,
)
ax4.set_ylabel("Students")
ax4.set_title("Effect on Student Teacher Ratio")
ax4.set_ylim((-3, 3))


fig.savefig(start.TABLE_PATH + "Figure3" + ".png", bbox_inches="tight")
