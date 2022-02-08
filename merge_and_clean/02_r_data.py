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
        "math_yr15std",
        "reading_yr15std",
        "district",
        "campus",
        "year",
        "pre_hisp",
        "pre_black",
        "pre_num",
        "pre_tenure",
        "pre_frpl",
        "pre_turnover",
    ]
)


col = r_data.loc[:, "class_size_3":"class_size_5"]
r_data["class_size_mean_elem"] = col.mean(axis=1)


r_data.to_csv(
    os.path.join(start.DATA_PATH, "clean", "r_data.csv"),
    sep=",",
)

# %% Ever treated
r_data_ever = data_school
r_data_ever["group"] = np.where(
    r_data_ever.doi_year == 2017,
    2017,
    np.where(
        r_data_ever.doi_year == 2018,
        2018,
        np.where(
            r_data_ever.doi_year == 2019,
            2019,
            np.where(r_data_ever.doi_year == 2020, 0, np.nan),
        ),
    ),
)
r_data_ever = r_data_ever.dropna(
    subset=[
        "group",
        "math",
        "reading",
        "district",
        "campus",
        "year",
        "pre_hisp",
        "pre_black",
        "pre_num",
        "pre_tenure",
        "pre_frpl",
        "pre_turnover",
    ]
)


col = r_data_ever.loc[:, "class_size_3":"class_size_5"]
r_data_ever["class_size_mean_elem"] = col.mean(axis=1)


r_data_ever.to_csv(
    os.path.join(start.DATA_PATH, "clean", "r_data_ever.csv"),
    sep=",",
)


# %% District Level


data_district = pd.read_csv(
    (start.DATA_PATH + "/clean/master_data_district.csv"), sep=","
)

r_data_district = data_school[data_school.distischarter == "N"]
r_data_district = r_data_district[r_data_district.eligible == True]
r_data_district["group"] = np.where(
    r_data_district.doi_year == 2017,
    2017,
    np.where(
        r_data_district.doi_year == 2018,
        2018,
        np.where(r_data_district.doi_year == 2019, 2019, 0),
    ),
)
r_data_district = r_data_district.dropna(
    subset=[
        "group",
        "math_yr15std",
        "reading_yr15std",
        "district",
        "campus",
        "year",
        "pre_hisp",
        "pre_black",
        "pre_num",
        "pre_tenure",
        "pre_frpl",
        "pre_turnover",
    ]
)


col = r_data_district.loc[:, "class_size_3":"class_size_5"]
r_data_district["class_size_mean_elem"] = col.mean(axis=1)


r_data_district.to_csv(
    os.path.join(start.DATA_PATH, "clean", "r_data_district.csv"),
    sep=",",
)
