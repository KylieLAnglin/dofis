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

plt.style.use("seaborn")
my_dpi = 96
plt.figure(figsize=(480 / my_dpi, 480 / my_dpi), dpi=my_dpi)


# %%

data = pd.read_csv(
    os.path.join(start.DATA_PATH, "clean", "master_data_school.csv"),
    sep=",",
    low_memory=False,
)
data = data[data.campischarter == "N"]

# %%
data = data[data.students_num > 50]
data = data[data.class_size_elem > 1]
data["Current District of Innovation"] = np.where(
    data.doi_year <= data.year, "Yes", "No"
)

# %%
fig = plt.figure(figsize=(15, 10))
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)


sns.boxplot(
    ax=ax1,
    x="year",
    y="teacher_uncertified",
    hue="Current District of Innovation",
    data=data[(data.year > 2016)],
)
ax1.set_ylabel("Proportion")
ax1.set_title("Proportion Uncertified Teachers")
ax1.set_xlabel("Year")

sns.boxplot(
    ax=ax2,
    x="year",
    y="teacher_out_of_field_fte",
    hue="Current District of Innovation",
    data=data[(data.year > 2016)],
)
ax2.set_ylabel("Proportion")
ax2.set_title("Proportion Out-of-Field Teachers")
ax2.set_xlabel("Year")


sns.boxplot(
    ax=ax3,
    x="year",
    y="class_size_elem",
    hue="Current District of Innovation",
    data=data[(data.year > 2016) & (~data.m_3rd_avescore.isnull())],
)
ax3.set_ylabel("Students")
ax3.set_title("Average Elementary Class Sizes")
ax3.set_xlabel("Year")

sns.boxplot(
    ax=ax4,
    x="year",
    y="stu_teach_ratio",
    hue="Current District of Innovation",
    data=data[(data.year > 2016)],
)
ax4.set_ylabel("Students")
ax4.set_title("Student Teacher Ratio")
ax4.set_xlabel("Year")

fig.savefig(
    start.TABLE_PATH + "formatted_results/AppendixC_FigureC1.pdf", bbox_inches="tight"
)

# %%
