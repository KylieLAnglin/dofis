# %%
import datetime
import os

import numpy as np
import pandas as pd

from dofis import start

pd.options.display.max_columns = 200

# %%
data_school = pd.read_csv((start.DATA_PATH + "/clean/master_data_school.csv"), sep=",")

# Exclude never-takers
r_data = data_school[data_school.campischarter == "N"]
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
        "campus",
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

r_data["teacher_uncertified_extreme"] = np.where(
    r_data.teacher_uncertified > 0.05, 1, 0
)
r_data["teacher_out_of_field_extreme"] = np.where(
    r_data.teacher_out_of_field_fte > 0.05, 1, 0
)
r_data["class_size_elem_extreme"] = np.where(r_data.class_size_elem > 25, 1, 0)
r_data["stu_teach_ratio_extreme"] = np.where(r_data.stu_teach_ratio > 18, 1, 0)


r_data.to_csv(
    os.path.join(start.DATA_PATH, "clean", "r_data.csv"),
    sep=",",
)
