# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import statsmodels.formula.api as smf

from dofis import start
from dofis.analysis.library import analysis

plt.style.use("seaborn")

# %%
df = pd.read_excel(start.TABLE_PATH + "results_uncertified_ag_raw_average" + ".xlsx")

df = pd.read_csv(start.DATA_PATH + "clean/r_data.csv")
df = df[df.year.isin([2016, 2017])]
df["treat"] = np.where(df.group == 2017, 1, 0)
df["post"] = np.where(df.year > 2016, 1, 0)
df["treat_post"] = df.treat * df.post

results = smf.ols("teacher_uncertified ~ 1 + treat + post + treatpost", data=df).fit()
results.summary()
# %%
fig = plt.figure(figsize=(15, 10))
ax1 = fig.add_subplot(111)

# Treated
ax1.plot(
    [2016, 2017],
    [0.0113 - 0.0036, 0.0113 - 0.0036 + 0.0035 - 0.0003],
    color="black",
    label="2017 Cohort",
    linewidth=1,
)

# Untreated
ax1.plot(
    [2016, 2017],
    [0.0113, 0.0113 + 0.0035],
    color="gray",
    label="Counterfactual",
    linewidth=1,
)


# Counterfactual
ax1.plot(
    [2016, 2017],
    [0.0113 - 0.0036, 0.0113 + 0.0035 - 0.0036],
    color="gray",
    linestyle="dotted",
    label="2018+ Cohorts",
    linewidth=1,
)

ax1.set_xlim([2015.75, 2017.25])
ax1.set_xticks([], fontsize=30)
ax1.set_ylim(-0.00, 0.02)
ax1.set_yticks([0.005, 0.01, 0.015, 0.02], fontsize=30)
ax1.set_ylabel("Proportion Uncertified Teachers", fontsize=20)

ax1.legend()

fig.savefig(start.TABLE_PATH + "Michigan_graph.pdf", bbox_inches="tight")

# %%
