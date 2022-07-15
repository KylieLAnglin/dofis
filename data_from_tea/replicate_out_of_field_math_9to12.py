# %%
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

# %%
classes = classes[classes["CLASS TYPE NAME"] == "ACADEMIC ACHIEVEMENT COURSE"]
classes = classes[classes["ROLE NAME"] == "TEACHER"]
classes = classes[classes["CAMPUS CHARTER TYPE NAME"] == "NOT A CHARTER SCHOOL"]
classes = classes[classes["DISTRICT CHARTER TYPE NAME"] == "NOT A CHARTER DISTRICT"]

# %%
classes = classes[classes["SUBJECT NAME"] == "MATHEMATICS"]
classes = classes[classes["GRADE LEVEL NAME"] == "GRADES 9-12"]

# %%
classes["SCRAMBLED UNIQUE ID"].nunique()

# %%
classes["PARTIAL FULL TIME EQUIVALENT"].astype("float").sum()

# %%
# Read files
teacher_datapath = os.path.join(start.DATA_PATH, "teachers", year)
pattern = "TEACHER_MASTER*.TXT"
teachers = build.concat_files(path=teacher_datapath, pattern=pattern)

# %%
teachers = teachers[teachers["ROLE NAME"] == "TEACHER"]
teachers = teachers[teachers["CAMPUS CHARTER TYPE NAME"] == "NOT A CHARTER SCHOOL"]
teachers = teachers[teachers["DISTRICT CHARTER TYPE NAME"] == "NOT A CHARTER DISTRICT"]
teachers = teachers[teachers["CAMPUS TYPE NAME"] == "INSTRUCTIONAL CAMPUS"]

# %%
teachers["CAMPUS GRADE GROUP NAME"].value_counts()
teachers = teachers[teachers["CAMPUS GRADE GROUP NAME"] == "HIGH SCHOOL"]
len(teachers)

# %% Certification
teacher_datapath = os.path.join(start.DATA_PATH, "teachers", year)
pattern = "STAFF_CERTIFICATION_1819*.csv"  # yr1819
certs = build.concat_files(path=teacher_datapath, pattern="CERTIFICATION_*.csv")
len(certs)

# %%
certs = certs[certs["ROLE_CREDENTIALED_FOR"] == "Teacher"]

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
certs = certs[certs["CREDENTIAL_TYPE"].isin(certifications)]
len(certs)

# %%
certs[
    "CERTIFICATE_EXPIRATION_DATE"
].value_counts()  # 2018-19 excluded expired certificates
certs["expiration"] = certs["CERTIFICATE_EXPIRATION_DATE"]
certs["expiration"] = np.where(
    certs.expiration.isnull(), "31AUG2050:00:00:00", certs.expiration
)
certs["expiration"] = certs["expiration"].astype(str).str[0:9]
certs["expiration"] = pd.to_datetime(certs.expiration)
certs = certs[certs["expiration"] > "2017-08-01"]
len(certs)
# %%
high_grades = ["Grades 8-12", "Grades 6-12", "Grades 7-12", "Grades 6-10"]
certs["certified_high"] = np.where(certs["CREDENTIALED_GRADES"].isin(high_grades), 1, 0)
certs = certs[certs.certified_high == 1]
len(certs)
# %%
certs["certified_math"] = np.where((certs["SUBJECT_AREA"] == "Mathematics"), 1, 0)
# certs = certs[certs.certified_math == 1]
len(certs)
# %%
certs["PERSONID_SCRAM"].nunique()

# certs = certs.drop_duplicates(subset=["PERSONID_SCRAM"], keep="first")
# certs["certified"] = 1

# %%
####
###
# Merge
###
####
classes_cert = classes.merge(
    certs,
    how="left",
    left_on="SCRAMBLED UNIQUE ID",
    right_on="PERSONID_SCRAM",
    indicator="_merge",
)
# %%
classes_cert["certified"] = np.where(
    classes_cert.certified.isnull(), 0, classes_cert.certified
)
classes_cert.certified.mean()


# %%
classes_cert = classes_cert.sort_values(
    by=["PERSONID_SCRAM", "certified"], ascending=True
)
teacher_all_classes_cert = classes_cert.drop_duplicates(
    subset=["SCRAMBLED UNIQUE ID"], keep="first"
)


teacher_all_classes_cert.certified.mean()
teacher_all_classes_cert.certified.value_counts()
# %%
course_requirements = pd.read_csv(
    "/Users/kla21002/Dropbox/Active/dofis/data/teachers/field_requirements.csv",
)  # %%

# %%
classes_requirements = classes.merge(
    course_requirements,
    left_on="CLASS NUMBER",
    right_on="class_number",
    how="outer",
    indicator="_acceptable_certs",
)
# %%
teacher_datapath = os.path.join(start.DATA_PATH, "teachers", year)
pattern = "STAFF_CERTIFICATION_1819*.csv"  # yr1819
full_certs = build.concat_files(path=teacher_datapath, pattern="CERTIFICATION_*.csv")
len(full_certs)


classes_requirements_met = classes_requirements.head(1000).merge(
    full_certs,
    left_on="cert_desc",
    right_on="FULLER_CERTIFICATE_DESCRIPTION",
    how="left",
)

# %%
