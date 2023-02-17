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

data = pd.read_csv(start.DATA_PATH + "clean/master_data_district.csv")
data = data[data.year >= 2016]
data = data[data.distischarter == 0]

# %%
data.sample()

# %%
data16 = data[data.year == 2016][
    "district",
]
