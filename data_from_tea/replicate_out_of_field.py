import os
import fnmatch

import pandas as pd
import numpy as np

from dofis import start
from dofis.data_from_tea.library import build
from dofis.data_from_tea.library import clean_tea

# %% Classes
year = "yr1819"
teacher_datapath = os.path.join(start.DATA_PATH, "teachers", year)
pattern = "TEACHER_CLASS*.TXT"
classes = build.concat_files(path=teacher_datapath, pattern=pattern)

classes = classes[classes["CLASS TYPE NAME"] == "ACADEMIC ACHIEVEMENT COURSE"]
classes = classes[classes["ROLE NAME"] == "TEACHER"]
classes = classes[classes["CAMPUS CHARTER TYPE NAME"] == "NOT A CHARTER SCHOOL"]
classes = classes[classes["DISTRICT CHARTER TYPE NAME"] == "NOT A CHARTER DISTRICT"]

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

classes = classes.rename(columns=vars_to_keep)

# %% High School Math

classes["teaches_math"] = np.where(
    classes["SUBJECT NAME"] == "MATHEMATICS", True, False
)
classes = classes[classes["teaches_math"] == 1]

classes["teaches_high"] = np.where(classes.grade_level == "GRADES 9-12", True, False)
classes = classes[classes["teaches_high"] == 1]

classes["teaches_math_high"] = np.where(
    (classes.teaches_math == True) & (classes.teaches_high == True), True, False
)

classes[classes.teaches_math_high == True].teacher_id.nunique()

classes["fte"] = pd.to_numeric(classes.fte, errors="coerce")
classes.fte.sum()


traditional_math_classes = [
    "ALGEBRA I (ALG 1)",
    "GEOMETRY (GEOM)",
    "ALGEBRA II (ALG2)",
    "PRECALCULUS (PRE CALC)",
    "ALGEBRA I",
]
df = classes[classes["CLASS NAME"].isin(traditional_math_classes)]
df.teacher_id.nunique()

# %%

# Read files
teacher_datapath = os.path.join(start.DATA_PATH, "teachers", year)
pattern = "TEACHER_MASTER*.TXT"

teachers = build.concat_files(path=teacher_datapath, pattern=pattern)

vars_to_keep = {
    "SCRAMBLED UNIQUE ID": "teacher_id",
    # "DISTRICT NUMBER": "district",
    # "DISTRICT NAME": "distname",
    # "CAMPUS NUMBER": "campus",
    # "CAMPUS NAME": "campname",
    # "CAMPUS GRADE GROUP NAME": "camp_grade_group",
    # "ROLE FULL TIME EQUIVALENT": "fte_teacher",
    # "EXPERIENCE": "experience",
}
teachers = teachers.rename(columns=vars_to_keep)
teachers.sort_values(by=["teacher_id"], axis=0)

len(teachers)
teachers = teachers[teachers["ROLE NAME"] == "TEACHER"]
teachers = teachers[teachers["CAMPUS CHARTER TYPE NAME"] == "NOT A CHARTER SCHOOL"]
teachers = teachers[teachers["DISTRICT CHARTER TYPE NAME"] == "NOT A CHARTER DISTRICT"]
len(teachers)

teachers["CAMPUS TYPE NAME"].value_counts()
teachers[teachers["CAMPUS TYPE NAME"] == "INSTRUCTIONAL CAMPUS"]
len(teachers)

teachers["CAMPUS GRADE GROUP NAME"].value_counts()
teachers = teachers[teachers["CAMPUS GRADE GROUP NAME"] == "HIGH SCHOOL"]

len(teachers)

teachers["SUBJECT AREA NAME 1"].value_counts()
df = teachers[teachers["SUBJECT AREA NAME 1"] == "MATHEMATICS"]
len(df)

df = teachers[
    (teachers["SUBJECT AREA NAME 1"] == "MATHEMATICS")
    | (teachers["SUBJECT AREA NAME 2"] == "MATHEMATICS")
]
len(df)

df = teachers[
    (teachers["SUBJECT AREA NAME 1"] == "MATHEMATICS")
    | (teachers["SUBJECT AREA NAME 2"] == "MATHEMATICS")
    | (teachers["SUBJECT AREA NAME 3"] == "MATHEMATICS")
]
len(df)

df = teachers[
    (teachers["SUBJECT AREA NAME 1"] == "MATHEMATICS")
    | (teachers["SUBJECT AREA NAME 2"] == "MATHEMATICS")
    | (teachers["SUBJECT AREA NAME 3"] == "MATHEMATICS")
    | (teachers["SUBJECT AREA NAME 4"] == "MATHEMATICS")
    | (teachers["SUBJECT AREA NAME 5"] == "MATHEMATICS")
]
len(df)

df = teachers[
    (teachers["SUBJECT AREA NAME 1"] == "MATHEMATICS")
    | (teachers["SUBJECT AREA NAME 2"] == "MATHEMATICS")
    | (teachers["SUBJECT AREA NAME 3"] == "MATHEMATICS")
    | (teachers["SUBJECT AREA NAME 4"] == "MATHEMATICS")
    | (teachers["SUBJECT AREA NAME 5"] == "MATHEMATICS")
    | (teachers["SUBJECT AREA NAME 6"] == "MATHEMATICS")
    | (teachers["SUBJECT AREA NAME 7"] == "MATHEMATICS")
    | (teachers["SUBJECT AREA NAME 8"] == "MATHEMATICS")
    | (teachers["SUBJECT AREA NAME 9"] == "MATHEMATICS")
    | (teachers["SUBJECT AREA NAME 10"] == "MATHEMATICS")
    | (teachers["SUBJECT AREA NAME 11"] == "MATHEMATICS")
]
len(df)
# %%
