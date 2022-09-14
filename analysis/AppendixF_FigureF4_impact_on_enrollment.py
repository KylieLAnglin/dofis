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
enrollment_agg = pd.read_excel(start.TABLE_PATH + "results_students_num_ag_raw.xlsx")

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
black_df = coef_df(black_agg)
hisp_df = coef_df(hisp_agg)
frpl_df = coef_df(frpl_agg)
enrollment_df = coef_df(enrollment_agg)


fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
colors = [
    "gray",
    "gray",
    "gray",
    "gray",
    "gray",
    "gray",
    "black",
    "black",
    "black",
    "black",
]

# Uncertified
ax1.scatter(
    x=black_df.year,
    marker="s",
    s=120,
    y=black_df["coef"],
    color=colors,
)
for pos, y, err, color in zip(
    black_df.year, black_df["coef"], black_df["errsig"], colors
):

    ax1.errorbar(pos, y, err, lw=2, capsize=4, capthick=4, color=color)

ax1.axhline(y=0, linestyle="--", color="black", linewidth=1)
ax1.set_xticks(black_df.year)

# ax1.xaxis.set_ticks_position("none")
# ax1.set_xticklabels(black_df.year)
# _ = ax1.set_xticklabels(
#     ["Pre5", "Pre4", "Pre3", "Pre2", "Pre1", "Post1", "Post2", "Post3"],
#     rotation=0,
# )
ax1.set_ylabel("Proportion")
ax1.set_title("Proportion Black Students")
ax1.set_ylim((-0.1, 0.1))

# Out of field
ax2.scatter(
    x=hisp_df.year,
    marker="s",
    s=120,
    y=hisp_df["coef"],
    color=colors,
)
for pos, y, err, color in zip(hisp_df.year, hisp_df["coef"], hisp_df["errsig"], colors):

    ax2.errorbar(pos, y, err, lw=2, capsize=4, capthick=4, color=color)

ax2.axhline(y=0, linestyle="--", color="black", linewidth=1)
ax2.set_xticks(hisp_df.year)

# ax2.xaxis.set_ticks_position("none")
# _ = ax2.set_xticklabels(
#     ["Pre5", "Pre4", "Pre3", "Pre2", "Pre1", "Post1", "Post2", "Post3"],
#     rotation=0,
# )
ax2.set_ylabel("Proportion")
ax2.set_title("Proportion Hispanic Students")
ax2.set_ylim((-0.1, 0.1))

# Class Size
ax3.scatter(
    x=black_df.year,
    marker="s",
    s=120,
    y=frpl_df["coef"],
    color=colors,
)
for pos, y, err, color in zip(frpl_df.year, frpl_df["coef"], frpl_df["errsig"], colors):

    ax3.errorbar(pos, y, err, lw=2, capsize=4, capthick=4, color=color)
ax3.set_xticks(frpl_df.year)

ax3.axhline(y=0, linestyle="--", color="black", linewidth=1)
ax3.xaxis.set_ticks_position("none")
# _ = ax3.set_xticklabels(
#     ["Pre5", "Pre4", "Pre3", "Pre2", "Pre1", "Post1", "Post2", "Post3"],
#     rotation=0,
# )
ax3.set_ylabel("Proportion")
ax3.set_title("Proportion FRPL Students")
ax3.set_ylim((-0.1, 0.1))

# Student-Teacher Ratio
ax4.scatter(
    x=enrollment_df.year,
    marker="s",
    s=120,
    y=enrollment_df["coef"],
    color=colors,
)
for pos, y, err, color in zip(
    enrollment_df.year, enrollment_df["coef"], enrollment_df["errsig"], colors
):

    ax4.errorbar(pos, y, err, lw=2, capsize=4, capthick=4, color=color)
ax4.set_xticks(enrollment_df.year)
ax4.axhline(y=0, linestyle="--", color="black", linewidth=1)
ax4.xaxis.set_ticks_position("none")
# _ = ax4.set_xticklabels(
#     ["Pre5", "Pre4", "Pre3", "Pre2", "Pre1", "Post1", "Post2", "Post3", ""],
#     rotation=0,
# )
ax4.set_ylabel("Students")
ax4.set_title("Number of Students")
ax4.set_ylim((-50, 50))
