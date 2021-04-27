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

from dofis.analysis.library import start

# get_ipython().run_line_magic('matplotlib', 'inline')
plt.style.use("seaborn")
my_dpi = 96
plt.figure(figsize=(480 / my_dpi, 480 / my_dpi), dpi=my_dpi)

# %%
data = pd.read_csv(start.data_path + "clean/r_data_district_2020_comparison.csv")

data[data.year == 2019].doi_year.value_counts().sort_index()


title_labels = {
    "avescores": "Average STAR",
    "math_yr15std": "Average Std. Math Scores",
    "reading_yr15std": "Average Std. Reading Scores",
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

monochrome = cycler("color", ["k"]) * cycler("linestyle", ["-", "--", ":", "-."])


# %%
def create_group_df(df, outcome):
    df["outcome"] = df[outcome]
    df = df[["year", "outcome"]]
    new_df = pd.DataFrame(df.groupby(["year"]).agg({"outcome": ["mean", "sem"]}))
    new_df = new_df.rename(columns={"mean": "score_mean", "sem": "score_se"})
    new_df["ub"] = new_df["outcome"]["score_mean"] + new_df["outcome"]["score_se"]
    new_df["lb"] = new_df["outcome"]["score_mean"] - new_df["outcome"]["score_se"]
    return new_df


outcome = "math"

df_treat2017 = create_group_df(data[data.doi_year == 2017], outcome=outcome)
df_treat2018 = create_group_df(data[data.doi_year == 2018], outcome=outcome)
df_treat2019 = create_group_df(data[data.doi_year == 2019], outcome=outcome)
df_treat2020 = create_group_df(data[data.doi_year == 2020], outcome=outcome)


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

# %% Cohort 1
outcome = "math_yr15std"
df_treat = create_group_df(data[data.doi_year == 2017], outcome=outcome)
df_comparison = create_group_df(data[data.doi_year != 2017], outcome=outcome)


fig, ax = plt.subplots(1, 1)
ax.set_prop_cycle(monochrome)

ax.plot(
    list(df_treat.index),
    df_treat["outcome"]["score_mean"],
    label="2016-17 DOI Implementers",
)
ax.plot(
    list(df_comparison.index),
    df_comparison["outcome"]["score_mean"],
    label="2018, 2019, and 2020 Cohorts",
)

ax.legend()
ax.fill_between(list(df_treat.index), df_treat.lb, df_treat.ub, alpha=0.2)
ax.fill_between(
    list(df_comparison.index), df_comparison.lb, df_comparison.ub, alpha=0.2
)


ax.axvline(x=2016.5, linestyle="-", color="black")


ax.set_title(title_labels[outcome])
ax.grid(False)

# %%
# %% Cohort 2
outcome = "math_yr15std"
df_treat = create_group_df(data[data.doi_year == 2018], outcome=outcome)
df_comparison = create_group_df(
    (data[~data.doi_year.isin([2017, 2018])]), outcome=outcome
)


fig, ax = plt.subplots(1, 1)
ax.set_prop_cycle(monochrome)

ax.plot(
    list(df_treat.index),
    df_treat["outcome"]["score_mean"],
    label="2017-18 Cohort",
)
ax.plot(
    list(df_comparison.index),
    df_comparison["outcome"]["score_mean"],
    label="2019 and 2020 Cohorts",
)

ax.legend()
ax.fill_between(list(df_treat.index), df_treat.lb, df_treat.ub, alpha=0.2)
ax.fill_between(
    list(df_comparison.index), df_comparison.lb, df_comparison.ub, alpha=0.2
)


ax.axvline(x=2017.5, linestyle="-", color="black")


ax.set_title(title_labels[outcome])
ax.grid(False)
# %%
# %% Cohort 3
outcome = "math_yr15std"
df_treat = create_group_df(data[data.doi_year == 2019], outcome=outcome)
df_comparison = create_group_df(
    (data[~data.doi_year.isin([2017, 2018, 2019])]), outcome=outcome
)


fig, ax = plt.subplots(1, 1)
ax.set_prop_cycle(monochrome)

ax.plot(
    list(df_treat.index),
    df_treat["outcome"]["score_mean"],
    label="2018-19 Cohort",
)
ax.plot(
    list(df_comparison.index),
    df_comparison["outcome"]["score_mean"],
    label="2020 Cohorts",
)

ax.legend()
ax.fill_between(list(df_treat.index), df_treat.lb, df_treat.ub, alpha=0.2)
ax.fill_between(
    list(df_comparison.index), df_comparison.lb, df_comparison.ub, alpha=0.2
)


ax.axvline(x=2018.5, linestyle="-", color="black")


ax.set_title(title_labels[outcome])
ax.grid(False)
# %%
