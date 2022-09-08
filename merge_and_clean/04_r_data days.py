# %%

import datetime
import os

import numpy as np
import pandas as pd


from dofis import start

pd.options.display.max_columns = 200


data_school = pd.read_csv((start.DATA_PATH + "/clean/master_data_school.csv"), sep=",")


r_data = data_school[data_school.campischarter == "N"]
r_data = r_data[r_data.eligible == True]
# r_data = r_data[r_data.group.isin(["opt-out", "2017", "2018", "2019"])]
r_data = r_data.rename(columns={"group": "doi_group"})
# r_data = r_data[r_data.year < 2021]
# r_data["teachers_uncertified"] = r_data.teachers_uncertified * 100
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
        "days_drop_outliers",
        # "math_yr15std",
        # "reading_yr15std",
        "district",
        "campus",
        "year",
    ]
)


col = r_data.loc[:, "class_size_3":"class_size_5"]
r_data["class_size_mean_elem"] = col.mean(axis=1)


r_data.to_csv(
    os.path.join(start.DATA_PATH, "clean", "r_data_days.csv"),
    sep=",",
)
