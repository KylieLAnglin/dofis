# TODO: Huge standard errors on student teacher ratio for urban schools
# %%
from re import sub
import pandas as pd
import numpy as np
import pandas as pd
from openpyxl import load_workbook
import scipy
import matplotlib.pyplot as plt

from dofis import start
from dofis.analysis.library import analysis

# %%
subgroups = ["average", "rural", "hispanic", "black", "frpl"]
outcomes = [
    "days",
    "days_before_third_week",
    "minutes",
]

results = {}
for outcome in outcomes:
    results[outcome] = {}
    for subgroup in subgroups:
        results[outcome][subgroup] = {}

# %%
graph_parameters = {
    "average": {"x_ticks_location": -0.3, "color": "black", "label": "Average Impact"},
    "rural": {"x_ticks_location": -0.2, "color": "blue", "label": "Rural Schools"},
    "black": {
        "x_ticks_location": -0.1,
        "color": "lightblue",
        "label": "Q4 Schools by % Black Students",
    },
    "hispanic": {
        "x_ticks_location": 0.10,
        "color": "green",
        "label": "Q4 Schools by % Hispanic Students",
    },
    "frpl": {
        "x_ticks_location": 0.2,
        "color": "teal",
        "label": "Q4 Schools by % FRPL Students",
    },
    "days": {
        "title": "Number of Instructional Days",
        "ylabel": "Days",
        "ylim": (-50, 50),
    },
    "days_before_third_week": {
        "title": "Number of Instructional Days before Third Week of August",
        "ylabel": "Days",
        "ylim": (-5, 5),
    },
    "minutes": {
        "title": "Number of Instructional Minutes",
        "ylabel": "Minutes",
        "ylim": (-10000, 10000),
    },
}


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
for subgroup in subgroups:
    results["days"][subgroup]["df"] = pd.read_excel(
        start.TABLE_PATH + "results_days_ag_raw_" + subgroup + ".xlsx"
    )

    results["days"][subgroup]["coef_df"] = coef_df(results["days"][subgroup]["df"])

    results["days_before_third_week"][subgroup]["df"] = pd.read_excel(
        start.TABLE_PATH + "results_days_before_third_week_ag_raw_" + subgroup + ".xlsx"
    )
    results["days_before_third_week"][subgroup]["coef_df"] = coef_df(
        results["days_before_third_week"][subgroup]["df"]
    )

    results["minutes"][subgroup]["df"] = pd.read_excel(
        start.TABLE_PATH + "results_minutes_ag_raw_" + subgroup + ".xlsx"
    )

    results["minutes"][subgroup]["coef_df"] = coef_df(
        results["minutes"][subgroup]["df"]
    )


# %%


fig = plt.figure(figsize=(15, 10))
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)


# Uncertified
for outcome, ax in zip(outcomes, [ax1, ax2, ax3, ax4]):
    for subgroup in subgroups:
        df = results[outcome][subgroup]["coef_df"]
        df = df[df.year >= -5]

        xs = [x + graph_parameters[subgroup]["x_ticks_location"] for x in df["year"]]

        color = graph_parameters[subgroup]["color"]
        ax.scatter(
            x=xs,
            marker="s",
            s=30,
            y=df["coef"],
            color=graph_parameters[subgroup]["color"],
            label=graph_parameters[subgroup]["label"],
        )
        for pos, y, err in zip(xs, df["coef"], df["errsig"]):
            ax.errorbar(pos, y, err, lw=2, capsize=2, capthick=2, color=color)

    ax.axhline(y=0, linestyle="--", color="black", linewidth=1)
    # ax.xaxis.set_ticks_position("none")
    ax.set_xticks(xs)
    ax.set_xticklabels(
        df["year"],
    )
    ax.set_ylabel(graph_parameters[outcome]["ylabel"])
    ax.set_title(graph_parameters[outcome]["title"])
    # ax.set_xlim((-0.5, 7.5))
    ax.set_ylim(graph_parameters[outcome]["ylim"])
    ax.axvline(0, color="gray")

ax.legend(loc="lower left", bbox_to_anchor=(1, 0.5))


# %%
