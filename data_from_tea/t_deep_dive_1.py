# %%
import pandas as pd
import numpy as np

from dofis import start
from dofis.data_from_tea.library import build

year = "yr1819"

teacher_datapath = start.DATA_PATH + "teachers/" + year

# %%
# teacher = "*38V5V024"
# teacher = "Q3550D048"
# teacher = "03065L144"
# teacher = "Y320Q0048"
teacher = "F32*1Q448"  # class = 03270100
year = "yr1819"

# %% Import courses
pattern = "TEACHER_CLASS*.TXT"
if year > "yr1819":
    pattern = "*TCHCLASS_REGION*csv"
classes = build.concat_files(path=teacher_datapath, pattern=pattern)

classes = classes.rename(
    columns={
        "CLASS NUMBER": "class_number",
        "SCRAMBLED UNIQUE ID": "teacher_id",
        "ROLE NAME": "role",
    }
)
classes = classes[classes.role == "TEACHER"]
classes = classes[classes.teacher_id == teacher]

# %% Import course requirements (only one must match to be in field)
course_requirements = pd.read_csv(
    start.DATA_PATH + "teachers/field_requirements.csv", dtype={"class_number": object}
)

# drop id (not available in data)
course_requirements = course_requirements.drop_duplicates(
    subset=["class_number", "cert_desc"]
)

# %%

classes_w_requirements = classes.merge(
    course_requirements,
    left_on="class_number",
    right_on="class_number",
    how="left",
    indicator="_merge_requirements",
)

# %% import certifications
pattern = "STAFF_CERTIFICATION_1819*.csv"
cert = build.concat_files(path=teacher_datapath, pattern=pattern)
cert = cert.rename(columns={"PID_SCRAM": "teacher_id"})
cert = cert[cert.teacher_id == teacher]

# %% Full long dataset
classes_w_requirements_and_certs = classes_w_requirements.merge(
    cert,
    left_on=["teacher_id", "cert_desc"],
    right_on=["teacher_id", "cert_desc"],
    how="left",
    indicator="_cert_match",
)
classes_w_requirements_and_certs["cert_match"] = np.where(
    classes_w_requirements_and_certs._cert_match == "both",
    1,
    np.where(classes_w_requirements_and_certs._merge_requirements == "both", 0, np.nan),
)

classes_w_requirements_and_certs = classes_w_requirements_and_certs.sort_values(
    by=["teacher_id", "class_number", "_cert_match"], ascending=False
)
# %% Keep first match or first non-match for each teacher's class
classes_w_requirements_and_certs = classes_w_requirements_and_certs.drop_duplicates(
    subset=["teacher_id", "class_number"], keep="first"
)

# %%
