# %%
import numpy as np
import pandas as pd
from dofis import start
from dofis.analysis.library import analysis, characteristics, tables

# %%
data = pd.read_csv(
    start.DATA_PATH + "clean/master_data_school.csv",
    sep=",",
    low_memory=False,
)

# %% Districts of innovation

school_df = pd.DataFrame(data.groupby(["campus"]).agg({"doi_year": "mean"}))
school_counts = pd.DataFrame(school_df.doi_year.value_counts(sort=False))
print(school_counts)
school_counts = school_counts.sort_index()
print("Cumulative count of DOIs in each year:")
print(school_counts.doi_year.cumsum())

# %% Not-yet districts of innovation
len(school_df[(school_df.doi_year > 2017)])
len(school_df[(school_df.doi_year > 2018)])
len(school_df[(school_df.doi_year > 2019)])
len(school_df[(school_df.doi_year > 2020)])

# %% Number of Ineligible Districts
data = data[data.distischarter == 0]

data17 = data[data.year == 2017]
data18 = data[data.year == 2018]
data19 = data[data.year == 2019]
data20 = data[data.year == 2020]

data17.eligible.value_counts()
data18.eligible.value_counts()
data19.eligible.value_counts()
data20.eligible.value_counts()
