import pandas as pd
import os
import fnmatch
import numpy as np
from dofis import start
from dofis.data_from_tea.library import clean_tea
from dofis.data_from_tea.library import build

year = "yr1718"
for year in [
    "yr1213",
    "yr1314",
    "yr1415",
    "yr1516",
    "yr1617",
    "yr1718",
    "yr1819",
    "yr1920",
    "yr2021",
    "yr2122",
]:
    # Read files
    teacher_datapath = os.path.join(start.DATA_PATH, "teachers", year)
    pattern = "TEACHER_MASTER*.TXT"

    if year > "yr1819":
        pattern = "*TEACHER_MASTER.csv"

    teachers = build.concat_files(path=teacher_datapath, pattern=pattern)
    if year < "yr1920":
        teachers = teachers[teachers["ROLE NAME"] == "TEACHER"]
    else:
        teachers = teachers[teachers["ROLEX"] == "TEACHER"]

    vars_to_keep = {
        "SCRAMBLED UNIQUE ID": "teacher_id",
        "DISTRICT NUMBER": "district",
        "DISTRICT NAME": "distname",
        "CAMPUS NUMBER": "campus",
        "CAMPUS NAME": "campname",
        "CAMPUS GRADE GROUP NAME": "camp_grade_group",
        "ROLE FULL TIME EQUIVALENT": "fte_teacher",
        "EXPERIENCE": "experience",
    }
    if year > "yr1819":
        vars_to_keep = {
            "PERSONID_SCRAM": "teacher_id",
            "DISTRICT": "district",
            "DISTNAME": "distname",
            "CAMPUS": "campus",
            "CAMPNAME": "campname",
            "GRADEGRP1X": "camp_grade_group",
            "PFTE": "fte_teacher",
            # "EXPERIENCE": "experience",
            #  "TOTALPAY": "pay",
        }
    teachers = clean_tea.filter_and_rename_cols(teachers, vars_to_keep)

    teachers.sort_values(by=["teacher_id"], axis=0)
    filename = "teachers_" + year + ".csv"
    teachers.to_csv(os.path.join(start.DATA_PATH, "teachers", filename))
