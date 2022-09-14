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


math_agg = pd.read_excel(
    start.TABLE_PATH + "results_w_nevertakers_math_yr15std_average_ag_raw.xlsx"
)
reading_agg = pd.read_excel(
    start.TABLE_PATH + "results_w_nevertakers_reading_yr15std_average_ag_raw.xlsx"
)
attendance_agg = pd.read_excel(
    start.TABLE_PATH + "results_w_nevertakers_perf_attendance_average_ag_raw.xlsx"
)


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

math_df = coef_df(math_agg)
reading_df = coef_df(reading_agg)
attendance_df = coef_df(attendance_agg)

fig = plt.figure(figsize=(15, 10))
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)

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
]

# Uncertified
ax1.scatter(
    x=math_df.year,
    marker="s",
    s=120,
    y=math_df["coef"],
    color=colors,
)
for pos, y, err, color in zip(math_df.year, math_df["coef"], math_df["errsig"], colors):

    ax1.errorbar(pos, y, err, lw=2, capsize=4, capthick=4, color=color)

ax1.axhline(y=0, linestyle="--", color="black", linewidth=1)
ax1.set_xticks(math_df.year)

ax1.set_ylabel("Effect Size")
ax1.set_title("Mathematics")
ax1.set_ylim((-0.5, 0.5))

# Out of field
ax2.scatter(
    x=reading_df.year,
    marker="s",
    s=120,
    y=reading_df["coef"],
    color=colors,
)
for pos, y, err, color in zip(
    reading_df.year, reading_df["coef"], reading_df["errsig"], colors
):

    ax2.errorbar(pos, y, err, lw=2, capsize=4, capthick=4, color=color)

ax2.axhline(y=0, linestyle="--", color="black", linewidth=1)
ax2.set_xticks(reading_df.year)


ax2.set_ylabel("Effect Size Estimate")
ax2.set_title("Reading")
ax2.set_ylim((-0.5, 0.5))

# Class Size
ax3.scatter(
    x=attendance_df.year,
    marker="s",
    s=120,
    y=attendance_df["coef"],
    color=colors,
)
for pos, y, err, color in zip(
    attendance_df.year, attendance_df["coef"], attendance_df["errsig"], colors
):

    ax3.errorbar(pos, y, err, lw=2, capsize=4, capthick=4, color=color)
ax3.set_xticks(attendance_df.year)

ax3.axhline(y=0, linestyle="--", color="black", linewidth=1)
ax3.xaxis.set_ticks_position("none")
# _ = ax3.set_xticklabels(
#     ["Pre5", "Pre4", "Pre3", "Pre2", "Pre1", "Post1", "Post2", "Post3"],
#     rotation=0,
# )
ax3.set_ylabel("Proportion")
ax3.set_title("Attendance")
ax3.set_ylim((-1, 1))
