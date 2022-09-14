# %%
import datetime
import os

import numpy as np
import pandas as pd

from dofis import start

pd.options.display.max_columns = 200

# %%

data_district = pd.read_csv(
    (start.DATA_PATH + "/clean/master_data_district.csv"), sep=","
)


# Exclude charters, inelgible districts, and never-takers
r_data = data_district[data_district.distischarter == "N"]
r_data = r_data[r_data.eligible == True]
r_data = r_data[r_data.group.isin(["2017", "2018", "2019", "2020+"])]
r_data = r_data.rename(columns={"group": "doi_group"})
r_data = r_data[r_data.year < 2021]
# %%
r_data["group"] = np.where(
    r_data.doi_year == 2017,
    2017,
    np.where(
        r_data.doi_year == 2018,
        2018,
        np.where(r_data.doi_year == 2019, 2019, 0),
    ),
)

r_data = r_data.dropna(
    subset=[
        "group",
        "district",
        "year",
        "pre_hisp",
        "pre_black",
        "pre_num",
        "pre_tenure",
        "pre_frpl",
        "pre_turnover",
        "pre_avescore",
    ]
)


col = r_data.loc[:, "class_size_3":"class_size_5"]
r_data["class_size_mean_elem"] = col.mean(axis=1)


r_data.to_csv(
    os.path.join(start.DATA_PATH, "clean", "r_data_district.csv"),
    sep=",",
)
