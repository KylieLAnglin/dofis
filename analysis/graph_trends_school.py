#!/usr/bin/env python
# coding: utf-8

# %%


import os
import sys

import matplotlib.pyplot as plt
import pandas as pd


from dofis import start

# get_ipython().run_line_magic('matplotlib', 'inline')
plt.style.use("seaborn")
my_dpi = 96
plt.figure(figsize=(480 / my_dpi, 480 / my_dpi), dpi=my_dpi)


# %%

data = pd.read_csv(
    os.path.join(start.DATA_PATH, "clean", "gdid_school.csv"),
    sep=",",
    low_memory=False,
)
data = data[data.doi == 1]
print(data.doi_year.value_counts())

data.sample()

# %%

# convert year to datetime
df = data.reset_index()
df["year_index"] = pd.to_datetime(df["year"], format="%Y")
df["campus_index"] = df.campus
df = df.set_index(["campus_index", "year_index"])
df[
    [
        "campus",
        "year",
        "doi_year",
        "treatpost",
        "yearpost",
        "post1",
        "math",
        "reading",
        "elem_math",
    ]
].sample(5)

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


title_labels = {
    "avescores": "Average STAR",
    "math": "Average Std. Math Scores",
    "reading": "Average Std. Reading Scores",
    "elem_math": "Elementary Math",
    "elem_reading": "Elementary Reading",
    "middle_math": "Middle School Math",
    "middle_reading": "Middle School Reading",
    "biology": "Biology",
    "algebra": "Algebra",
    "eng1": "English I",
    "students_num": "Number of Students",
    "students_hisp": "Percent Hispanic",
    "stu_teach_ratio": "Student Teacher Ratio",
    "teachers_uncertified": "Percent Uncertified Teachers",
    "class_size_5": "5th Grade Class Size",
}

outcome = "math"
# Create cycler object. Use any styling from above you please
df_treat2017 = create_group_df(data[data.doi_year == 2017], outcome=outcome)
df_treat2018 = create_group_df(data[data.doi_year == 2018], outcome=outcome)
df_treat2019 = create_group_df(data[data.doi_year == 2019], outcome=outcome)
df_treat2020 = create_group_df(data[data.doi_year == 2020], outcome=outcome)
df_treat2021 = create_group_df(data[data.doi_year == 2021], outcome=outcome)

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

ax.plot(
    list(df_treat2020.index),
    df_treat2020["outcome"]["score_mean"],
    label="2019-20 DOI Implementers",
)


ax.legend()
ax.fill_between(list(df_treat2017.index), df_treat2017.lb, df_treat2017.ub, alpha=0.2)
ax.fill_between(list(df_treat2018.index), df_treat2018.lb, df_treat2018.ub, alpha=0.2)
ax.fill_between(list(df_treat2019.index), df_treat2019.lb, df_treat2019.ub, alpha=0.2)
ax.fill_between(list(df_treat2020.index), df_treat2020.lb, df_treat2020.ub, alpha=0.2)

ax.axvline(x=2016.5, linestyle="-", color="black")
ax.axvline(x=2017.5, linestyle="--", color="black")
ax.axvline(x=2018.5, linestyle=":", color="black")

ax.set_title(title_labels[outcome])
ax.grid(False)

# fig.savefig(
#     start.table_path + "trends_by_adoption_" + outcome + ".png", bbox_inches="tight"
# )

# %%
data = pd.read_csv(
    os.path.join(start.DATA_PATH, "clean", "master_data_school.csv"),
    sep=",",
    low_memory=False,
)

outcome = "math_yr15std"
df_treat2017 = create_group_df(data[data.doi_year == 2017], outcome=outcome)
df_treat2018 = create_group_df(data[data.doi_year == 2018], outcome=outcome)
df_treat2019 = create_group_df(data[data.doi_year == 2019], outcome=outcome)
df_treat2020 = create_group_df(data[(data.doi_year == 2020)], outcome=outcome)

df_control = create_group_df(data[data.doi == False], outcome=outcome)
df_charter = create_group_df(data[data.distischarter == False], outcome=outcome)


fig, ax = plt.subplots(1, 1)

ax.plot(
    list(df_treat2017.index),
    df_treat2017["outcome"]["score_mean"],
    label="2016-17 DOI Implementers",
    linestyle="-",
    color="black",
)
ax.plot(
    list(df_treat2018.index),
    df_treat2018["outcome"]["score_mean"],
    label="2017-18 DOI Implementers",
    linestyle="--",
    color="black",
)
ax.plot(
    list(df_treat2019.index),
    df_treat2019["outcome"]["score_mean"],
    label="2018-19 DOI Implementers",
    linestyle=":",
    color="black",
)


ax.plot(
    list(df_treat2020.index),
    df_treat2020["outcome"]["score_mean"],
    label="2019-20 Implementers",
    linestyle="--",
    color="gray",
)


ax.plot(
    list(df_charter.index),
    df_charter["outcome"]["score_mean"],
    label="Charter School Districts",
    linestyle=":",
    color="gray",
)


ax.plot(
    list(df_control.index),
    df_control["outcome"]["score_mean"],
    label="Control",
    linestyle="-",
    color="gray",
)

ax.legend()
# ax.fill_between(list(df_treat2017.index), df_treat2017.lb, df_treat2017.ub, alpha=0.2)
# ax.fill_between(list(df_treat2018.index), df_treat2018.lb, df_treat2018.ub, alpha=0.2)
# ax.fill_between(list(df_treat2019.index), df_treat2019.lb, df_treat2019.ub, alpha=0.2)
# ax.fill_between(list(df_control.index), df_control.lb, df_control.ub, alpha=0.2)


ax.axvline(x=2016.5, linestyle="-", color="black")
ax.axvline(x=2017.5, linestyle="--", color="black")
ax.axvline(x=2018.5, linestyle=":", color="black")

ax.grid(False)

# fig.savefig(
#     start.table_path + "trends_by_adoption_" + outcome + ".png", bbox_inches="tight"
# )
# %%
outcome = "math"
df_treat = create_group_df(data[data.doi == True], outcome=outcome)
df_control = create_group_df(data[data.doi == False], outcome=outcome)
df_charter = create_group_df(data[data.distischarter == False], outcome=outcome)


fig, ax = plt.subplots(1, 1)

ax.plot(
    list(df_treat.index),
    df_treat["outcome"]["score_mean"],
    label="DOIs",
    linestyle="-",
    color="black",
)
ax.plot(
    list(df_charter.index),
    df_charter["outcome"]["score_mean"],
    label="Charter Schools",
    linestyle="--",
    color="black",
)
ax.axvline(x=2016, linestyle="-", color="black")


ax.legend()


ax.set_title(title_labels[outcome])
ax.grid(False)


# %%
