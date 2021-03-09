# %%
import os
import sys

import matplotlib
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from patsy import dmatrices

from dofis.analysis.library import start


plt.style.use("seaborn")


# %%

data = pd.read_csv(
    os.path.join(start.data_path, "clean", "master_data_district.csv"),
    sep=",",
    low_memory=False,
)

data = data[data.distischarter == 0]

data15 = data[data.year == 2015]
data16 = data[data.year == 2016]
data17 = data[data.year == 2017]
data18 = data[data.year == 2018]
data19 = data[data.year == 2019]


# Use 2015-16 data for descriptives bc one district not in 2018-19 dataset.

# %% Number of districts
print("Number of traditional public school districts in Texas in 2019:")
print(data19.district.nunique())

# %% Eligibility

print("Number of ineligible TPSDs in 2019:")
print(data16[(data16.eligible19 == 0) & (data16.doi != 1)].district.nunique())

print("Number of eligible non-DOIs as of June 2019")
print(data16.loc[(data16.doi == 0) & (data16.eligible19 == 1)].district.nunique())

print("Some districts lost eligibility")
print(data16.loc[(data16.doi == 1) & (data16.eligible19 == 0)].district.nunique())


print("What % of traditional public school district were eligible in 2015?")
print(data15.eligible.mean())
print("And in 2015-16")
print(data16.eligible.mean())
print("And in 2016-17")
print(data17.eligible.mean())
print("And in 2017-18?")
print(data18.eligible.mean())
print("And in 2018-19?")
print(data19.eligible.mean())

# %% Districts of Innovation


print("Number of DOIs as of June 2019")
print(data16.loc[data16.doi == 1].district.nunique())


print("What percent of districts are DOIs as of June 2019?")
print(
    data16.loc[data16.doi == 1].district.nunique()
    / data16[data16.distischarter == 0].district.nunique()
)

print(data16.doi_year.value_counts().sort_index())

print(len(data16[(data16.doi == 1) & (data16.doi_year.isnull())]))

# %%

print("Number of DOIs with missing implementation year:")
print(len(data16[(data16.doi == 1) & (data16.doi_year.isnull())]))
# %% Adoption over time figure


district_df = pd.DataFrame(data.groupby(["district"]).agg({"doi_year": "mean"}))
district_counts = pd.DataFrame(district_df.doi_year.value_counts(sort=False))
print(district_counts)
district_counts = district_counts.sort_index()
print("Cumulative count of DOIs in each year:")
print(district_counts.doi_year.cumsum())

my_dpi = 96
plt.figure(figsize=(480 / my_dpi, 480 / my_dpi), dpi=my_dpi)

# Pre
plt.plot(district_counts.index, district_counts.doi_year.cumsum(), color="black")
plt.xticks([int(i) for i in list(district_counts.index)])

plt.ylabel("Number of Districts")
plt.title("Texas District of Innovation Adoption Over Time")
plt.xlabel("Test Year (Spring)", size="medium")
plt.grid(True, alpha=0.6)


plt.ylim(0, 1022)
# txt = "Notes: Statistics are as of June 202-. "
# "There are ten Districts of Innovation (with missing Innovation Plans) \n "
# "that are not included in the figure. "
# "As of 2019, there were 1022 traditional public school districts in Texas."
# # plt.figtext(0.5, -0.01, txt, wrap=True, horizontalalignment="center", fontsize=8)

plt.savefig(start.table_path + "takeup.png", dpi=600, bbox_inches="tight")
plt.show()


# %% Geography of Districts of Innovation
print(str(data16[data16.doi == 1].type_urban.mean().round(2)), "Urban")
print(str(data16[data16.doi == 1].type_suburban.mean().round(2)), "Suburban")
print(str(data16[data16.doi == 1].type_town.mean().round(2)), "Town")
print(str(data16[data16.doi == 1].type_rural.mean().round(2)), "Rural")

# %% School Takeup

data_school = pd.read_csv(
    os.path.join(start.data_path, "clean", "master_data_school.csv"),
    sep=",",
    low_memory=False,
)

school_df = pd.DataFrame(data_school.groupby(["campus"]).agg({"doi_year": "mean"}))
school_counts = pd.DataFrame(school_df.doi_year.value_counts(sort=False))
school_counts = school_counts.sort_index()


my_dpi = 96
plt.figure(figsize=(480 / my_dpi, 480 / my_dpi), dpi=my_dpi)


plt.plot(school_counts.index, school_counts.doi_year.cumsum(), color="black")

plt.xticks([int(i) for i in list(school_counts.index)])

plt.ylabel("Number of Schools")
plt.title("Texas District of Innovation Adoption Over Time")
plt.xlabel("Test Year (Spring)", size="medium")
plt.grid(True, alpha=0.6)


txt = "Notes: Statistics are as of June 2019. "
plt.figtext(0.5, -0.01, txt, wrap=True, horizontalalignment="center", fontsize=8)

plt.show()

# %%
