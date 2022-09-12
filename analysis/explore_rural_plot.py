# %%


import os
import sys

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from cycler import cycler
from matplotlib import lines, markers
from scipy import stats

from dofis import start

data = pd.read_csv(start.DATA_PATH + "clean/master_data_school.csv")
data = data[(data.year < 2020) & (data.year > 2012)]
data = data[data.pre_rural == 1]
# %%

plt.style.use("seaborn")


my_dpi = 96
# fig = plt.figure(figsize=(480 / my_dpi, 480 / my_dpi), dpi=my_dpi)
fig = plt.figure()
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)

# %%


# %% Visual Impact by Subject


def create_group_df(df, outcome):
    df["outcome"] = df[outcome]
    df = df[["year", "outcome"]]
    new_df = pd.DataFrame(df.groupby(["year"]).agg({"outcome": ["mean", "sem"]}))
    new_df = new_df.rename(columns={"mean": "score_mean", "sem": "score_se"})
    new_df["ub"] = new_df["outcome"]["score_mean"] + new_df["outcome"]["score_se"]
    new_df["lb"] = new_df["outcome"]["score_mean"] - new_df["outcome"]["score_se"]
    return new_df


# %%
title_labels = {
    "math_yr15std": "Average Std. Math Scores",
    "reading_yr15std": "Average Std. Reading Scores",
    "teacher_uncertified": "Percent Uncertified Teachers",
    "class_size_elem": "Average Elementary Class Size",
}


for outcome, ax in zip(title_labels, [ax1, ax2, ax3, ax4]):
    df_treat2017 = create_group_df(data[data.group == "2017"], outcome=outcome)
    df_treat2018 = create_group_df(data[data.group == "2018"], outcome=outcome)
    df_treat2019 = create_group_df(data[data.group == "2019"], outcome=outcome)
    df_treat2020 = create_group_df(
        data[data.group == "2020+"],
        outcome=outcome,
    )
    df_control = create_group_df(data[data.group == "opt-out"], outcome=outcome)
    monochrome = cycler("color", ["k"]) * cycler("linestyle", ["-", "--", ":", "-."])

    ax.set_prop_cycle(monochrome)

    ax.plot(
        list(df_treat2017.index),
        df_treat2017["outcome"]["score_mean"],
        label="2016-17 DOI Implementers",
        color="gray",
        linestyle="dotted",
    )
    ax.plot(
        list(df_treat2018.index),
        df_treat2018["outcome"]["score_mean"],
        label="2017-18 DOI Implementers",
        color="gray",
        linestyle="solid",
    )
    ax.plot(
        list(df_treat2019.index),
        df_treat2019["outcome"]["score_mean"],
        label="2018-19 DOI Implementers",
        color="black",
        linestyle="dotted",
    )

    ax.plot(
        list(df_treat2020.index),
        df_treat2020["outcome"]["score_mean"],
        label="2019-20 to 2020-21 DOI Implementers",
        color="black",
        linestyle="dashed",
    )

    ax.plot(
        list(df_control.index),
        df_control["outcome"]["score_mean"],
        label="Districts Opting Out",
        color="black",
        linestyle="solid",
    )

    ax.fill_between(
        list(df_treat2017.index), df_treat2017.lb, df_treat2017.ub, alpha=0.2
    )
    ax.fill_between(
        list(df_treat2018.index), df_treat2018.lb, df_treat2018.ub, alpha=0.2
    )
    ax.fill_between(
        list(df_treat2019.index), df_treat2019.lb, df_treat2019.ub, alpha=0.2
    )

    ax.fill_between(
        list(df_treat2020.index), df_treat2020.lb, df_treat2020.ub, alpha=0.2
    )

    ax.fill_between(list(df_control.index), df_control.lb, df_control.ub, alpha=0.2)

    ax.set_title(title_labels[outcome])
    ax.grid(False)

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    if outcome in ["math_yr15std", "reading_yr15std"]:
        ax.get_xaxis().set_ticks([])
        ax.set_ylim([-0.75, 0.75])
    else:
        ax.set_xticks(
            [2013, 2014, 2015, 2016, 2017, 2018, 2019],
            ["'13", "-14", "'15", "'16", "'17", "'18", "'19"],
        )

    if outcome == "teachers_uncertified":
        ax.set_ylim([0, 0.01])

    if outcome == "class_size_elem":
        ax.set_ylim([16, 22])


# Put a legend to the right of the current axis
ax.legend(loc="lower left", bbox_to_anchor=(1, 0.5))
fig.show()

fig.savefig(start.TABLE_PATH + "FigureC1.png", bbox_inches="tight")

# %%
