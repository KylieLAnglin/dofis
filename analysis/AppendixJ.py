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

import seaborn as sns
from dofis import start

# %%

data = pd.read_csv(start.DATA_PATH + "clean/master_data_school.csv")
data = data[data.year > 2014]
data = data[data.doi == 1]
data["current_doi"] = np.where((data.year >= data.doi_year) & (data.doi == 1), 1, 0)
sns.boxplot(data=data, x="year", y="teacher_uncertified", hue="current_doi")

# %%
