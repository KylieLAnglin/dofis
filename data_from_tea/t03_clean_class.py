import os
import fnmatch

import pandas as pd
import numpy as np

from library import start
from library import build
from library import clean_tea


for year in ["yr1213", "yr1314", "yr1415", "yr1516", "yr1617", "yr1718", "yr1819"]:
    teacher_datapath = os.path.join(start.data_path, "teachers", year)
    pattern = "TEACHER_CLASS*.TXT"
    classes = build.concat_files(path=teacher_datapath, pattern=pattern)

    classes = classes[classes["ROLE NAME"] == "TEACHER"]

    vars_to_keep = {
        "SCRAMBLED UNIQUE ID": "teacher_id",
        "DISTRICT NUMBER": "district",
        "DISTRICT NAME": "distname",
        "CAMPUS NUMBER": "campus",
        "CAMPUS NAME": "campname",
        "SUBJECT AREA CODE": "subject_area_code",
        "SUBJECT AREA NAME": "subject_area",
    }

    classes = clean_tea.filter_and_rename_cols(classes, vars_to_keep)

    classes["math"] = np.where(classes.subject_area == "MATHEMATICS", True, False)
    classes["science"] = np.where(classes.subject_area == "SCIENCE", True, False)

    teachers = classes[["teacher_id", "campus", "math", "science"]]

    teachers = teachers.groupby(["teacher_id", "campus"]).max()

    teachers.sort_values(by=["teacher_id"], axis=0)
    filename = "classes_" + year + ".csv"
    teachers.to_csv(os.path.join(start.data_path, "teachers", filename))
