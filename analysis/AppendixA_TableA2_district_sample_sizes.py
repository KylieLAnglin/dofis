# %%
import numpy as np
import pandas as pd
from dofis import start
from dofis.analysis.library import analysis, characteristics, tables

# %%
data = pd.read_csv(
    start.DATA_PATH + "clean/master_data_district.csv",
    sep=",",
    low_memory=False,
)

# %% Districts of innovation

district_df = pd.DataFrame(data.groupby(["district"]).agg({"doi_year": "mean"}))
district_counts = pd.DataFrame(district_df.doi_year.value_counts(sort=False))
print(district_counts)
district_counts = district_counts.sort_index()
print("Cumulative count of DOIs in each year:")
print(district_counts.doi_year.cumsum())

# %% Not-yet districts of innovation
len(district_df[(district_df.doi_year > 2017)])
len(district_df[(district_df.doi_year > 2018)])
len(district_df[(district_df.doi_year > 2019)])
len(district_df[(district_df.doi_year > 2020)])
len(district_df[(district_df.doi_year > 2021)])


# %% Number of Ineligible Districts
data = data[data.distischarter == 0]
data[(data.eligible == 1) & (data.doi == 0)].district.nunique()


data17 = data[data.year == 2017]
data18 = data[data.year == 2018]
data19 = data[data.year == 2019]
data20 = data[data.year == 2020]

data17.eligible.value_counts()
data18.eligible.value_counts()
data19.eligible.value_counts()
data20.eligible.value_counts()
