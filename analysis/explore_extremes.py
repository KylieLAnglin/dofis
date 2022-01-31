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

# %%

plt.style.use("seaborn")
my_dpi = 96
plt.figure(figsize=(480 / my_dpi, 480 / my_dpi), dpi=my_dpi)


# %%

data = pd.read_csv(
    os.path.join(start.DATA_PATH, "clean", "master_data_school.csv"),
    sep=",",
    low_memory=False,
)
data[data.year == 2019].doi_year.value_counts().sort_index()


# %%
data[
    [
        "campus",
        "campname",
        "year",
        "distischarter",
        "doi",
        "doi_year",
        "class_size_1",
        "class_size_2",
    ]
].sort_values(by=["class_size_1"], ascending=False).head(50)
# %%
data[(data.year == 2019) & (data.class_size_1 > 25) & (data.distischarter == 0)][
    [
        "campus",
        "campname",
        "year",
        "doi",
        "doi_year",
        "distischarter",
        "class_size_1",
        "class_size_2",
        "class_size_3",
    ]
].sort_values(by="class_size_1")

# %%
data["active_doi"] = np.where(data.year >= data.doi_year, 1, 0)
data[
    (data.year == 2019) & (data.class_size_1 > 25) & (data.distischarter == 0)
].active_doi.mean()
len(data[(data.year == 2019) & (data.class_size_1 > 25) & (data.distischarter == 0)])
# %%
data[
    (data.year == 2018) & (data.class_size_1 > 25) & (data.distischarter == 0)
].active_doi.mean()

# %%
data[
    (data.year == 2017) & (data.class_size_1 > 25) & (data.distischarter == 0)
].active_doi.mean()

# %%
data[
    (data.year == 2015) & (data.class_size_1 > 25) & (data.distischarter == 0)
].active_doi.mean()
len(data[(data.year == 2015) & (data.class_size_1 > 25) & (data.distischarter == 0)])
# %%
