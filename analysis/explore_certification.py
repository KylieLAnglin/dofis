# %%
import pandas as pd
import os
from dofis import start


data = pd.read_csv(
    os.path.join(start.DATA_PATH, "clean", "master_data_school.csv"),
    sep=",",
    low_memory=False,
)

data = data[data.year == 2018]
data.teacher_secondary_math_outoffield.sum()
# %%
