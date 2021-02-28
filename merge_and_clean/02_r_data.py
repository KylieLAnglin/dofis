# %%
import datetime
import os

import numpy as np
import pandas as pd

from dofis.merge_and_clean.library import clean_final
from dofis.merge_and_clean.library import clean_for_merge
from dofis.merge_and_clean.library import start

pd.options.display.max_columns = 200


data_district = pd.read_csv(
    start.data_path + "clean/" + "master_data_district.csv", sep=","
)

# %% Charter Comparison

r_data = data_district
r_data["group"] = np.where(
    r_data.distischarter == True,
    0,
    np.where(
        r_data.doi_year == 2017,
        2017,
        np.where(
            r_data.doi_year == 2018,
            2018,
            np.where(r_data.doi_year == 2019, 2019, np.nan),
        ),
    ),
)
r_data = r_data.dropna(
    subset=["group", "elem_math", "middle_math", "alg_std", "district", "year"]
)

r_data.to_csv(
    os.path.join(start.data_path, "clean", "r_data_district_charter_comparison.csv"),
    sep=",",
)


# %%
r_data = data_district
r_data["group"] = np.where(
    r_data.doi_year == 2017,
    2017,
    np.where(
        r_data.doi_year == 2018,
        2018,
        np.where(r_data.doi_year == 2019, 2019, np.nan),
    ),
)
r_data = r_data.dropna(
    subset=["group", "elem_math", "middle_math", "alg_std", "district", "year"]
)

r_data.to_csv(
    os.path.join(start.data_path, "clean", "r_data_district_notyet_comparison.csv"),
    sep=",",
)

# %%
r_data = data_district
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
        "elem_math",
        "middle_math",
        "alg_std",
        "district",
        "year",
    ]
)

r_data.to_csv(
    os.path.join(start.data_path, "clean", "r_data_district_2020_comparison.csv"),
    sep=",",
)


####
#   School
###


# %%
data_school = pd.read_csv(
    start.data_path + "clean/" + "master_data_school.csv", sep=","
)

# %% Charter Comparison

r_data = data_school
r_data["group"] = np.where(
    r_data.distischarter == True,
    0,
    np.where(
        r_data.doi_year == 2017,
        2017,
        np.where(
            r_data.doi_year == 2018,
            2018,
            np.where(r_data.doi_year == 2019, 2019, np.nan),
        ),
    ),
)
r_data = r_data.dropna(subset=["group", "elem_math", "campus", "year"])

r_data.to_csv(
    os.path.join(start.data_path, "clean", "r_data_elem_charter_comparison.csv"),
    sep=",",
)

r_data = r_data.dropna(subset=["group", "middle_math", "campus", "year"])


r_data.to_csv(
    os.path.join(start.data_path, "clean", "r_data_middle_charter_comparison.csv"),
    sep=",",
)


# %%
r_data = data_school
r_data["group"] = np.where(
    r_data.doi_year == 2017,
    2017,
    np.where(
        r_data.doi_year == 2018,
        2018,
        np.where(r_data.doi_year == 2019, 2019, np.nan),
    ),
)
r_data = r_data.dropna(subset=["group", "elem_math", "campus", "year"])

r_data.to_csv(
    os.path.join(start.data_path, "clean", "r_data_school_notyet_comparison.csv"),
    sep=",",
)

# %%
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
        "teachers_uncertified",
    ]
)

r_data["class_size_mean_elem"] = col.mean(axis=1)


r_data.to_csv(
    os.path.join(start.data_path, "clean", "r_data_school_2020_comparison.csv"),
    sep=",",
)


elem = r_data.dropna(
    subset=[
        "elem_math",
        "elem_reading",
    ]
)
col = elem.loc[:, "class_size_3":"class_size_5"]
elem["class_size_mean_elem"] = col.mean(axis=1)


elem.to_csv(
    os.path.join(start.data_path, "clean", "r_data_elem_2020_comparison.csv"),
    sep=",",
)


middle = r_data.dropna(
    subset=["group", "middle_math", "middle_reading", "campus", "year"]
)

middle.to_csv(
    os.path.join(start.data_path, "clean", "r_data_middle_2020_comparison.csv"),
    sep=",",
)

high = r_data.dropna(
    subset=["group", "algebra", "biology", "eng1_std", "campus", "year"]
)

high.to_csv(
    os.path.join(start.data_path, "clean", "r_data_high_2020_comparison.csv"),
    sep=",",
)

# %%


r_data = data_school
r_data["group"] = np.where(
    ((r_data.doi_year == 2020) | (r_data.doi == False))
    & (r_data.distischarter == False),
    0,
    np.where(
        r_data.doi_year == 2017,
        2017,
        np.where(
            r_data.doi_year == 2018,
            2018,
            np.where(r_data.doi_year == 2019, 2019, np.nan),
        ),
    ),
)
r_data = r_data.dropna(subset=["group", "math", "reading", "campus", "year"])

high.to_csv(
    os.path.join(start.data_path, "clean", "r_data_school_controls_comparison.csv"),
    sep=",",
)


# %%
