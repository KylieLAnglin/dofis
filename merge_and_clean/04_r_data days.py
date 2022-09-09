# %%

import datetime
import os

import numpy as np
import pandas as pd


from dofis import start

pd.options.display.max_columns = 200


data_school = pd.read_csv((start.DATA_PATH + "/clean/master_data_school.csv"), sep=",")


r_data = data_school[data_school.campischarter == "N"]
r_data = r_data[r_data.eligible == True]
# r_data = r_data[r_data.group.isin(["opt-out", "2017", "2018", "2019"])]
r_data = r_data.rename(columns={"group": "doi_group"})
# r_data = r_data[r_data.year < 2021]
# r_data["teachers_uncertified"] = r_data.teachers_uncertified * 100
# %%
r_data["group"] = np.where(
    r_data.doi_year == 2017,
    2017,
    np.where(
        r_data.doi_year == 2018,
        2018,
        np.where(r_data.doi_year == 2019, 2019, 0),
    ),
)

r_data = r_data.dropna(
    subset=[
        "group",
        "days_drop_outliers",
        # "math_yr15std",
        # "reading_yr15std",
        "district",
        "campus",
        "year",
    ]
)


col = r_data.loc[:, "class_size_3":"class_size_5"]
r_data["class_size_mean_elem"] = col.mean(axis=1)


r_data.to_csv(
    os.path.join(start.DATA_PATH, "clean", "r_data_days.csv"),
    sep=",",
)


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
    if time < group:  # if pre-treatment year, limit to year and year - 1
        did_df = df[(df[time_var] == time) | (df[time_var] == time - 1)]

    elif (
        time >= group
    ):  # if post-treatment year, limit to year and year before group first implemented
        did_df = df[
            (df[time_var] == time) | (df[time_var] == group - 1)
        ]  # limit to two years

    did_df = did_df[
        (did_df[group_var] == group)
        | (did_df[group_var] > time)
        | (did_df[group_var] == 0)
    ]  # limit to two groups

    did_df["treat"] = np.where(did_df[group_var] == group, 1, 0)
    did_df["post"] = np.where(did_df[time_var] == time, 1, 0)
    did_df["treat_post"] = did_df.treat * did_df.post

    return did_df
# %%
import statsmodels.formula.api as smf
import statsmodels.api as sm
def did(
    outcome: str,
    group_var: str,
    group: int,
    time_var: str,
    time: int,
    cluster_var: str,
    df: pd.DataFrame,
    verbose=True,
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
    if verbose:
        print(res.summary())
    return res

# %%
did(outcome = "minutes", group_var = "group", group = 2018, time_var="year", time=2018, cluster_var="district", df = r_data)
# %%



