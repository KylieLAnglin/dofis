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

data = pd.read_csv(start.DATA_PATH + "clean/master_data_school.csv")
data = data[data.year >= 2016]
data = data[data.distischarter == 0]

# %%
data.sample()

# %%
data16 = data[data.year == 2016][["district", "campus", "teacher_uncertified"]].rename(
    columns={"teacher_uncertified": "teacher_uncertified16"}
)
data17 = data[data.year == 2017][["district", "campus", "teacher_uncertified"]].rename(
    columns={"teacher_uncertified": "teacher_uncertified17"}
)
data18 = data[data.year == 2018][["district", "campus", "teacher_uncertified"]].rename(
    columns={"teacher_uncertified": "teacher_uncertified18"}
)
data19 = data[data.year == 2019][["district", "campus", "teacher_uncertified"]].rename(
    columns={"teacher_uncertified": "teacher_uncertified19"}
)
data20 = data[data.year == 2020][["district", "campus", "teacher_uncertified"]].rename(
    columns={"teacher_uncertified": "teacher_uncertified20"}
)
# %%
df = data[data.year == 2020]
for dataset in [data16, data17, data18, data19]:
    df = df.merge(
        dataset,
        left_on=["district", "campus"],
        right_on=["district", "campus"],
        how="left",
    )

# %%
temp_df = df[df.doi_year == 2019]
temp_df = temp_df[temp_df.students_num > 400]
temp_df["difference"] = temp_df.teacher_uncertified19 - temp_df.teacher_uncertified18
temp_df.sort_values(by=["difference"], ascending=False).head(5)
# %%
temp_df = df[df.doi_year == 2018]
# temp_df = temp_df[temp_df.students_num > 400]
temp_df["difference"] = temp_df.teacher_uncertified19 - temp_df.teacher_uncertified17
len(temp_df[temp_df.difference > 0.2])
temp_df.sort_values(by=["difference"], ascending=False).head(5)
temp_df[temp_df.district == 68901]
# %%
temp_df = df[df.doi_year == 2017]
temp_df = temp_df[temp_df.students_num > 400]
temp_df["difference"] = temp_df.teacher_uncertified19 - temp_df.teacher_uncertified16
len(temp_df[temp_df.difference > 0.2])
temp_df.sort_values(by=["difference"], ascending=False).head(5)

# %%
temp_df[temp_df.district == 68901]
# %%
temp_df = df[df.doi == 0]
temp_df = temp_df[temp_df.campischarter == 0]
temp_df["difference"] = temp_df.teacher_uncertified19 - temp_df.teacher_uncertified17
len(temp_df[temp_df.difference > 0.2])
temp_df.sort_values(by=["difference"], ascending=False).head(5)

# %%
