# %%
import os

import numpy as np
import pandas as pd

from library import start

IF_TEACHER_NOT_IN_CERT_DF_SET_AS = "missing"
# SECONDARY_VALUES = ["HIGH SCHOOL", "MIDDLE SCHOOL", "JUNIOR HIGH SCHOOL"]
SECONDARY_VALUES = ["HIGH SCHOOL"]
YEARS = ["yr1213", "yr1314", "yr1415", "yr1516", "yr1617", "yr1718", "yr1819"]

TEACHER_FILEPATH = start.data_path + "/teachers/"

# %% Descriptives in 2014-15
YEAR = "yr1415"
CERTIFICATION_FILE = "teacher_cert_" + YEAR + ".csv"
TEACHER_FILE = "teachers_" + YEAR + ".csv"
CLASSES_FILE = "classes_" + YEAR + ".csv"

certification = pd.read_csv(TEACHER_FILEPATH + CERTIFICATION_FILE).rename(
    columns={"district": "district_cert"}
)
teachers = pd.read_csv(TEACHER_FILEPATH + TEACHER_FILE)
teachers["teacher"] = 1
classes = pd.read_csv(TEACHER_FILEPATH + CLASSES_FILE)


df = teachers.merge(certification, how="left", on="teacher_id", indicator="cert_merge")
df = df.merge(classes, how="left", on=["teacher_id", "campus"])

NUMERIC_COLUMNS = [
    "fte_teacher",
    "standard",
    "cert_area_math",
    "cert_area_science",
    "cert_area_math_high",
    "cert_area_science_high",
]

df["high_school"] = np.where(df.camp_grade_group == "HIGH SCHOOL", True, False)
df["math_high"] = df.math * df.high_school
df["science_high"] = df.science * df.high_school


df[NUMERIC_COLUMNS] = df[NUMERIC_COLUMNS].apply(pd.to_numeric, errors="coerce")

school_df = df.groupby(
    [
        "campus",
        "campname",
        "camp_grade_group",
        "district",
        "district_cert",
        "high_school",
    ]
).sum()


district_df = df.groupby(["district"]).sum()

df["state"] = "Texas"

state_df = df.groupby(["state"]).sum()
state_df = state_df.drop(columns=["Unnamed: 0", "district", "campus", "district_cert"])
