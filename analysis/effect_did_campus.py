#!/usr/bin/env python
# coding: utf-8

# %%
import os
import sys

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from openpyxl import load_workbook

from dofis.analysis.library import start
from dofis.analysis.library import analysis


# %%

data = pd.read_csv(
    os.path.join(start.data_path, "clean", "r_data_school_2020_comparison.csv"),
    sep=",",
    low_memory=False,
)

data.sample()


# %%
did_df = data[
    ((data.group == 0) | (data.group == 2017))
    & ((data.year == 2016) | (data.year == 2019))
]

did_df["treat"] = np.where(did_df.group == 2017, 1, 0)
did_df["post"] = np.where(did_df.year == 2019, 1, 0)
did_df["treat_post"] = did_df.treat * did_df.post


mod = smf.ols("math_yr15std ~ 1 + treat + post + treat_post", did_df)
res = mod.fit(cov_type="cluster", cov_kwds={"groups": did_df["district"]})
print(res.summary())


# %%
def simple_did_df(
    group_var: str,
    group: int,
    time_var: str,
    time: int,
    df: pd.DataFrame,
):
    """Subsets a dataframe so that it only contains two groups
    and two time periods,

    Args:
        group_var (str): column containing group variable
        group (int): value in group column of dataframe to be treated
        time_var (str): column containing time variable
        time (int): value in time column of dataframe to be post
        df (pd.DataFrame): dataframe containing group and time columns

    Returns:
        pd.DataFrame: Untreated rows during one pre period, treat and untreated in one post
        new treatm, post, and treat_post columns
    """
    did_df = df[
        (df[time_var] == time) | (df[time_var] == group - 1)
    ]  # limit to two years
    did_df = did_df[
        (data[group_var] == group) | (data[group_var] > time) | (data[group_var] == 0)
    ]  # limit to two groups

    did_df["treat"] = np.where(did_df[group_var] == group, 1, 0)
    did_df["post"] = np.where(did_df[time_var] == time, 1, 0)
    did_df["treat_post"] = did_df.treat * did_df.post

    return did_df


def did(
    outcome: str,
    group_var: str,
    group: int,
    time_var: str,
    time: int,
    cluster_var: str,
    df: pd.DataFrame,
):
    """Estimate simple two-group two-time Diff-in-Diff

    Args:
        outcome (str): outcome column
        group_var (str): implementation group column with time of implementation where 0 indicates never treated
        group (int): implementation group of interest
        time_var (str): time column (should be in same units as group var)
        time (int): time of interest (pre-time is one less this value)
        cluster_var (str): cluster id column
        df (pd.DataFrame): dataset containing outcome, group_var, time_var, and cluster_var

    Returns:
        [type]: [description]
    """
    did_df = simple_did_df(
        group_var=group_var, group=group, time_var=time_var, time=time, df=df
    )
    mod = smf.ols(outcome + " ~ 1 + treat + post + treat_post", did_df)
    res = mod.fit(cov_type="cluster", cov_kwds={"groups": did_df[cluster_var]})
    print(res.summary())
    return res


did(
    outcome="math_yr15std",
    group_var="group",
    group=2017,
    time_var="year",
    time=2019,
    cluster_var="district",
    df=data,
)

# %%


def dids(
    outcome: str, group_var: str, time_var: str, cluster_var: str, df: pd.DataFrame
):

    groups = np.sort(df[df.group != 0][group_var].unique())
    times = np.sort(df[df[time_var] > df[time_var].min()][time_var].unique())
    group_time_combos = [
        {"group": group, "time": time} for time in times for group in groups
    ]

    group_results = {int(group): {} for group in groups}

    for combo in group_time_combos:
        group = combo["group"]
        time = combo["time"]

        did_result = did(
            outcome=outcome,
            group_var=group_var,
            group=group,
            time_var=time_var,
            time=time,
            cluster_var=cluster_var,
            df=df,
        )

        group_results[group][time] = did_result

    return group_results


math_results = dids(
    outcome="math_yr15std",
    group_var="group",
    time_var="year",
    cluster_var="district",
    df=data,
)

# %%
