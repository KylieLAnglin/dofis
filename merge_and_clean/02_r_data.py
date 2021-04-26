# %%
import datetime
import os

import numpy as np
import pandas as pd

from dofis.merge_and_clean.library import clean_final
from dofis.merge_and_clean.library import clean_for_merge
from dofis.merge_and_clean.library import start

pd.options.display.max_columns = 200


data_school = pd.read_csv((start.data_path + "/clean/master_data_school.csv"), sep=",")


##
#
##
r_data = data_school
r_data["group"] = np.where(
    r_data.doi_year == 2017,
    2017,
    np.where(
        r_data.doi_year == 2018,
        2018,
        np.where(
            r_data.doi_year == 2019, 2019, np.where(r_data.doi_year == 2020, 0, np.nan)
        ),
    ),
)
r_data = r_data.dropna(
    subset=[
        "group",
        "math",
        "reading",
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
    os.path.join(start.data_path, "clean", "r_data_school_2020_comparison.csv"),
    sep=",",
)

# %% District Level


data_district = pd.read_csv(
    (start.data_path + "/clean/master_data_district.csv"), sep=","
)

##
#
##
r_data_district = data_district
r_data_district["group"] = np.where(
    r_data_district.doi_year == 2017,
    2017,
    np.where(
        r_data_district.doi_year == 2018,
        2018,
        np.where(
            r_data_district.doi_year == 2019,
            2019,
            np.where(r_data_district.doi_year == 2020, 0, np.nan),
        ),
    ),
)
r_data_district = r_data_district.dropna(
    subset=[
        "group",
        "math",
        "reading",
        "district",
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
    os.path.join(start.data_path, "clean", "r_data_district_2020_comparison.csv"),
    sep=",",
)

# %%
