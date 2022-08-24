# %%
import matplotlib.pyplot as plt
import pandas as pd

from dofis import start

# %%
data = pd.read_csv(
    start.DATA_PATH + "clean/master_data_district.csv",
    sep=",",
    low_memory=False,
)

# %%
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

plt.ylabel("Number of Districts of Innovation")
plt.xlabel("Test Year (Spring)", size="medium")
plt.grid(True, alpha=0.6)


plt.ylim(0, 1022)
plt.savefig(start.TABLE_PATH + "AppendixA_FigureA1.png", dpi=600, bbox_inches="tight")
plt.show()

# %%
