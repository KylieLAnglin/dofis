# %%
import pandas as pd
import os
from dofis import start


data = pd.read_csv(
    os.path.join(start.DATA_PATH, "clean", "master_data_school.csv"),
    sep=",",
    low_memory=False,
)
data = data[data.distischarter == 0]
data = data[data.year == 2018]


print(data.teacher_secondary_math.sum())
print("According to TEA, there are 13559 9-12 mathematics teachers.")

# %%

data.teacher_secondary_math_outoffield.sum()

# %%
df = pd.read_csv(start.DATA_PATH + "tea/certification_rates_long.csv")
df = df[df.year == 2018]

print(df.teacher_secondary_math.sum())
print("According to TEA, there are 13559 9-12 mathematics teachers.")

# %%
