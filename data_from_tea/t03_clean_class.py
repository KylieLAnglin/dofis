import os
import fnmatch

import pandas as pd
import numpy as np

from dofis import start
from dofis.data_from_tea.library import build
from dofis.data_from_tea.library import clean_tea


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
    teacher_datapath = os.path.join(start.DATA_PATH, "teachers", year)
    pattern = "TEACHER_CLASS*.TXT"
    if year > "yr1819":
        pattern = "*TCHCLASS_REGION*csv"
    classes = build.concat_files(path=teacher_datapath, pattern=pattern)

    # classes = classes[classes["CLASS TYPE NAME"] == "ACADEMIC ACHIEVEMENT COURSE"]
    if year <= "yr1819":
        classes = classes[classes["ROLE NAME"] == "TEACHER"]
        classes = classes[classes["CAMPUS CHARTER TYPE NAME"] == "NOT A CHARTER SCHOOL"]
        classes = classes[
            classes["DISTRICT CHARTER TYPE NAME"] == "NOT A CHARTER DISTRICT"
        ]

    if year > "yr1819":
        classes = classes[classes["ROLEX"] == "TEACHER"]
        classes = classes[classes["CAMP_CHARTTYPEX"] == "NOT A CHARTER SCHOOL"]
        classes = classes[classes["DIST_CHARTTYPEX"] == "NOT A CHARTER DISTRICT"]

    vars_to_keep = {
        "SCRAMBLED UNIQUE ID": "teacher_id",
        "DISTRICT NUMBER": "district",
        "DISTRICT NAME": "distname",
        "CAMPUS NUMBER": "campus",
        "CAMPUS NAME": "campname",
        "SUBJECT AREA CODE": "subject_area_code",
        "SUBJECT AREA NAME": "subject_area",
        "GRADE LEVEL CODE": "grade_level_code",
        "GRADE LEVEL NAME": "grade_level",
        "PARTIAL FULL TIME EQUIVALENT": "fte",
    }

    if year > "yr1819":
        vars_to_keep = {
            "PERSONID_SCRAM": "teacher_id",
            "DISTRICT": "district",
            "DISTNAME": "distname",
            "CAMPUS": "campus",
            "CAMPNAME": "campname",
            "SUBJAREA": "subject_area_code",
            "SUBJAREAX": "subject_area",
            "GRADE_LEVEL": "grade_level_code",
            "GRADE_LEVELX": "grade_level",
            "PFTE_SUM": "fte",
        }
    classes = clean_tea.filter_and_rename_cols(classes, vars_to_keep)

    # classes["teaches_math"] = np.where(
    #     classes.subject_area == "MATHEMATICS", True, False
    # )

    classes["teaches_math"] = np.where(
        classes.subject_area == "MATHEMATICS", True, False
    )

    classes["teaches_science"] = np.where(
        classes.subject_area == "SCIENCE", True, False
    )
    classes["teaches_cte"] = np.where(
        classes.subject_area == "CAREER & TECHNOLOGY EDUCATION", True, False
    )

    classes["teaches_high"] = np.where(
        classes.grade_level == "GRADES 9-12", True, False
    )

    classes["teaches_math_high"] = np.where(
        (classes.teaches_math == True) & (classes.teaches_high == True), True, False
    )

    class_variables = list(classes.filter(like="teaches", axis=1).columns)
    variables_to_keep = ["teacher_id", "campus", "fte"] + class_variables

    teachers = classes[variables_to_keep]

    teachers = teachers.groupby(["teacher_id"]).max()

    teachers.sort_values(by=["teacher_id"], axis=0)
    filename = "classes_" + year + ".csv"
    teachers.to_csv(os.path.join(start.DATA_PATH, "teachers", filename))
