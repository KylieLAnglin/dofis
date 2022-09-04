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

# %%
# graph_parameters = {"teacher_uncertified": {"import_file": "results_uncertified_ag_raw.xlsx"}}
graph_parameters = {
    "teacher_uncertified": {
        "average": {"x_ticks_location": 0.20, "color": "black"},
        "rural": {"x_ticks_location": 0.10, "color": "red"},
        "urban": {"x_ticks_location": 0.0, "color": "orange"},
        "black": {"x_ticks_location": -0.1, "color": "green"},
        "hispanic": {"x_ticks_location": -0.20, "color": "blue"},
    },
    "teacher_out_of_field": {
        "average": {},
        "rural": {},
        "urban": {},
        "black": {},
        "hispanic": {},
    },
    "class_size_elem": {
        "average": {},
        "rural": {},
        "urban": {},
        "black": {},
        "hispanic": {},
    },
    "stu_teach_ratio": {
        "average": {},
        "rural": {},
        "urban": {},
        "black": {},
        "hispanic": {},
    },
}


# %%
def coef_df(df: pd.DataFrame):
    coefs = []
    ses = []
    for row in [0, 1, 2, 3, 4, 5, 6, 7]:
        coef = df.loc[row]["disag.att"]
        se = df.loc[row]["disag.se"]
        coefs.append(coef)
        ses.append(se)

    coef_df = pd.DataFrame(
        {
            "coef": coefs,
            "err": ses,
            "year": [-4, -3, -2, -1, 1, 2, 3, 4],
        }
    )
    coef_df["lb"] = coef_df.coef - (1.96 * coef_df.err)
    coef_df["ub"] = coef_df.coef + (1.96 * coef_df.err)
    coef_df["errsig"] = coef_df.err * 1.96
    return coef_df


# %%
for subgroup in ["average", "rural", "urban", "black", "hispanic"]:

    graph_parameters["teacher_uncertified"][subgroup]["df"] = pd.read_excel(
        start.TABLE_PATH + "results_uncertified_disag_raw_" + subgroup + ".xlsx"
    )

    graph_parameters["teacher_uncertified"][subgroup]["coef_df"] = coef_df(
        graph_parameters["teacher_uncertified"][subgroup]["df"]
    )
# %%

# TODO: ADD FRPL and low student achievement
# TODO: Add legend
# TODO: Decide on color scheme
# TODO: Add remaining outcomes

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
# colors = ["gray", "gray", "gray", "gray", "black", "black", "black", "black"]

outcome = "teacher_uncertified"
subgroup = "average"

# Uncertified
for subgroup in ["average", "rural", "urban", "black", "hispanic"]:
    df = graph_parameters[outcome][subgroup]["coef_df"]

    xs = [
        x + graph_parameters[outcome][subgroup]["x_ticks_location"]
        for x in pd.np.arange(df.shape[0])
    ]
    color = graph_parameters[outcome][subgroup]["color"]
    ax1.scatter(
        x=xs,
        marker="s",
        s=30,
        y=df["coef"],
        color=graph_parameters[outcome][subgroup]["color"],
    )
    for pos, y, err in zip(xs, df["coef"], df["errsig"]):
        ax1.errorbar(pos, y, err, lw=2, capsize=2, capthick=2, color=color)

ax1.axhline(y=0, linestyle="--", color="black", linewidth=1)
# ax1.xaxis.set_ticks_position("none")
ax1.set_xticks(xs)
ax1.set_xticklabels(
    ["Pre4", "Pre3", "Pre2", "Pre1", "Post1", "Post2", "Post3", "Post4"],
)
ax1.set_ylabel("Proportion")
ax1.set_title("Proportion Uncertified Teachers")
ax1.set_xlim((-0.5, 7.5))
ax1.set_ylim((-0.05, 0.05))

# %%
