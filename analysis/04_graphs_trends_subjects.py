#!/usr/bin/env python
# coding: utf-8

# %%
import os

import matplotlib.pyplot as plt
import pandas as pd
from cycler import cycler


from dofis import start

# get_ipython().run_line_magic('matplotlib', 'inline')
plt.style.use("seaborn")
my_dpi = 96
plt.figure(figsize=(480 / my_dpi, 480 / my_dpi), dpi=my_dpi)


# %%

df = pd.read_csv(
    os.path.join(start.DATA_PATH, "clean", "gdid_subject.csv"),
    sep=",",
    low_memory=False,
)
df[df.year == 2019].doi_year.value_counts().sort_index()
# %%


def create_group_df(df, outcome):
    df["outcome"] = df[outcome]
    df = df[["year", "outcome"]]
    new_df = pd.DataFrame(df.groupby(["year"]).agg({"outcome": ["mean", "sem"]}))
    new_df = new_df.rename(columns={"mean": "score_mean", "sem": "score_se"})
    new_df["ub"] = new_df["outcome"]["score_mean"] + new_df["outcome"]["score_se"]
    new_df["lb"] = new_df["outcome"]["score_mean"] - new_df["outcome"]["score_se"]
    return new_df


# %% Visual Impact by Subject
outcome = "score_std"
data = df[df.math_test == True]

df_treat2017 = create_group_df(data[data.doi_year == 2017], outcome=outcome)
df_treat2018 = create_group_df(data[data.doi_year == 2018], outcome=outcome)
df_treat2019 = create_group_df(data[data.doi_year == 2019], outcome=outcome)

monochrome = cycler("color", ["k"]) * cycler("linestyle", ["-", "--", ":", "-."])

fig, ax = plt.subplots(1, 1)
ax.set_prop_cycle(monochrome)

ax.plot(
    list(df_treat2017.index),
    df_treat2017["outcome"]["score_mean"],
    label="2016-17 DOI Implementers",
)
ax.plot(
    list(df_treat2018.index),
    df_treat2018["outcome"]["score_mean"],
    label="2017-18 DOI Implementers",
)
ax.plot(
    list(df_treat2019.index),
    df_treat2019["outcome"]["score_mean"],
    label="2018-19 DOI Implementers",
)

ax.legend()
ax.fill_between(list(df_treat2017.index), df_treat2017.lb, df_treat2017.ub, alpha=0.2)
ax.fill_between(list(df_treat2018.index), df_treat2018.lb, df_treat2018.ub, alpha=0.2)
ax.fill_between(list(df_treat2019.index), df_treat2019.lb, df_treat2019.ub, alpha=0.2)

ax.axvline(x=2016.5, linestyle="-", color="black")
ax.axvline(x=2017.5, linestyle="--", color="black")
ax.axvline(x=2018.5, linestyle=":", color="black")

# ax.set_title(title_labels[outcome])
ax.grid(False)

# %%
