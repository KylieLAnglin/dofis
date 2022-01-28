import os
import fnmatch

import pandas as pd
import numpy as np

from dofis import start
from dofis.data_from_tea.library import build
from dofis.data_from_tea.library import clean_tea

# %% Classes
year = "yr1718"
teacher_datapath = os.path.join(start.DATA_PATH, "teachers", year)
pattern = "TEACHER_CLASS*.TXT"
classes = build.concat_files(path=teacher_datapath, pattern=pattern)

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

classes["teaches_math"] = np.where(
    classes["SUBJECT NAME"] == "MATHEMATICS", True, False
)
classes["teaches_high"] = np.where(classes.grade_level == "GRADES 9-12", True, False)
classes = classes[classes["teaches_high"] == 1]

classes["teaches_math_high"] = np.where(
    (classes.teaches_math == True) & (classes.teaches_high == True), True, False
)


classes["fte"] = pd.to_numeric(classes.fte, errors="coerce")


traditional_math_classes = [
    "ALGEBRA I (ALG 1)",
    "GEOMETRY (GEOM)",
    "ALGEBRA II (ALG2)",
    "PRECALCULUS (PRE CALC)",
    "ALGEBRA I",
]
df = classes[classes["CLASS NAME"].isin(traditional_math_classes)]
df.teacher_id.nunique()

classes = classes[classes["CLASS TYPE NAME"] == "ACADEMIC ACHIEVEMENT COURSE"]
classes = classes[classes["ROLE NAME"] == "TEACHER"]
classes = classes[classes["CAMPUS CHARTER TYPE NAME"] == "NOT A CHARTER SCHOOL"]
classes = classes[classes["DISTRICT CHARTER TYPE NAME"] == "NOT A CHARTER DISTRICT"]
classes = classes[classes["teaches_math"] == 1]
classes = classes[classes["teaches_math_high"] == 1]

# %%
classes[classes.teaches_math_high == True].teacher_id.nunique()
classes.fte.sum()

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
    # | (teachers["SUBJECT AREA NAME 11"] == "MATHEMATICS")
]
len(df)
# %% Certification
teacher_datapath = os.path.join(start.DATA_PATH, "teachers", year)
FILE_PATTERNS = {
    "yr1213": "CERTIFICATION*.TXT",
    "yr1314": "CERTIFICATION*.TXT",
    "yr1415": "CERTIFICATION_*.csv",
    "yr1516": "CERTIFICATION_*.csv",
    "yr1617": "CERTIFICATION_*.csv",
    "yr1718": "CERTIFICATION_*.csv",
    "yr1819": "STAFF_CERTIFICATION_1819*.csv",
}

pattern = FILE_PATTERNS[year]
cert = build.concat_files(path=teacher_datapath, pattern=pattern)
len(cert)

VARS_TO_KEEP_YR1819 = {
    "PID_SCRAM": "teacher_id",
    "DISTRICT": "district",
    "cert_role": "cert_role",
    "cert_type": "cert_type",
    "exp_dt": "expiration",
    "cert_level": "cert_level",
    "cert_area": "cert_area",
    "cert_field": "subject",
}

VARS_TO_KEEP_YR1516_TO_YR1718 = {
    "PERSONID_SCRAM": "teacher_id",
    "DISTRICT": "district",
    "ROLE_CREDENTIALED_FOR": "cert_role",
    "CREDENTIAL_TYPE": "cert_type",
    "CERTIFICATE_EXPIRATION_DATE": "expiration",
    "CERTIFICATION_LEVEL": "cert_level",
    "SUBJECT_AREA": "cert_area",
    "SUBJECT": "cert_subject",
}

year_vars = {"yr1718": VARS_TO_KEEP_YR1516_TO_YR1718, "yr1819": VARS_TO_KEEP_YR1819}

cert = cert.rename(columns=year_vars[year])

cert["cert_role"].value_counts()
cert = cert[cert["cert_role"] == "Teacher"]
len(cert)

cert["cert_type"].value_counts()
certifications = [
    "Standard",
    "Provisional",
    "Probationary",
    "Probationary Extension",
    "Probationary Second Extension",
    "One Year",
    "Visiting International Teacher"
    # "Professional", # Excluded from out of field
    # "Standard Professional" # Excluded from out of field ,
]
cert = cert[cert.cert_type.isin(certifications)]
len(cert)

cert["expiration"].value_counts()  # 2018-19 excluded expired certificates
cert["expiration2"] = np.where(
    cert.expiration.isnull(), "31AUG2050:00:00:00", cert.expiration
)
cert["expiration2"] = cert["expiration2"].astype(str).str[0:9]
cert["expiration2"] = pd.to_datetime(cert.expiration2)
cert = cert[cert["expiration2"] > "2017-08-01"]
len(cert)

# Need to deal with effective dates after start of school year
cert[
    "CERTIFICATE_EFFECTIVE_DATE"
].value_counts()  # 2018-19 excluded expired certificates
cert["effective"] = np.where(
    cert["CERTIFICATE_EFFECTIVE_DATE"].isnull(),
    "31AUG1900:00:00:00",
    cert["CERTIFICATE_EFFECTIVE_DATE"],
)
cert["effective"] = cert["effective"].astype(str).str[0:9]
cert["effective"] = pd.to_datetime(cert.effective)
cert = cert[cert["effective"] <= "2017-08-01"]
len(cert)

cert["certified"] = 1


high_grades = ["Grades 8-12", "Grades 6-12", "Grades 7-12", "Grades 6-10"]
cert["certified_high"] = np.where(cert["CREDENTIALED_GRADES"].isin(high_grades), 1, 0)


cert["certified_high_math"] = np.where(
    (cert["cert_area"] == "Mathematics") & (cert.certified_high == 1), 1, 0
)

cert[cert.certified_high_math == 1].teacher_id.nunique()

cert = cert.sort_values(
    by=["teacher_id", "certified_high_math", "certified_high"], ascending=False
)
cert = cert.drop_duplicates(subset=["teacher_id"], keep="first")

cert.certified.value_counts()

cert.certified_high.value_counts()

cert.certified_high_math.value_counts()
cert[cert.certified_high_math == 1].teacher_id.nunique()

# %%
classes_cert = classes.merge(
    cert[["teacher_id", "certified", "certified_high", "certified_high_math"]],
    how="left",
    left_on="teacher_id",
    right_on="teacher_id",
    indicator="_merge",
)

classes_cert["certified"] = np.where(
    classes_cert.certified.isnull(), 0, classes_cert.certified
)

classes_cert["certified_high"] = np.where(
    classes_cert.certified_high.isnull(), 0, classes_cert.certified_high
)

classes_cert["certified_high_math"] = np.where(
    classes_cert.certified_high_math.isnull(), 0, classes_cert.certified_high_math
)


classes_cert[classes_cert.certified == 0].teacher_id.nunique()

classes_cert.certified_high_math.value_counts()
classes_cert[classes_cert.certified_high_math == 0].teacher_id.nunique()
classes_cert[
    classes_cert.certified_high_math == 0
].teacher_id.nunique() / classes_cert.teacher_id.nunique()


classes_cert[classes_cert.certified_high_math == 0].fte.sum() / classes_cert.fte.sum()


# %%
course_requirements = pd.read_csv(
    "/Users/kla21002/Dropbox/Active/dofis/data/teachers/field_requirements.csv",
)  # %%

# %%
