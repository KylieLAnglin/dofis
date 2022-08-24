# %%
import pandas as pd
import numpy as np

from dofis import start
from dofis.data_from_tea.library import build

year = "yr2021"

teacher_datapath = start.DATA_PATH + "teachers/" + year

# %% Import courses
pattern = "TEACHER_CLASS*.TXT"
if year > "yr1819":
    pattern = "*TCHCLASS_REGION*csv"
classes = build.concat_files(path=teacher_datapath, pattern=pattern)

classes = classes.rename(
    columns={
        "SERVICE": "class_number",
        "PERSONID_SCRAM": "teacher_id",
        "ROLEX": "role",
    }
)

classes = classes[classes.role == "TEACHER"]

# %% Import course requirements (only one must match to be in field)
course_requirements = pd.read_csv(
    start.DATA_PATH + "teachers/field_requirements.csv", dtype={"class_number": object}
)
# drop id (not available in data)
course_requirements = course_requirements.drop_duplicates(
    subset=["class_number", "cert_desc"]
)


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

# %% Address fuzzy certification requirements
classes_w_requirements_and_certs["cert_match"] = np.where(
    classes_w_requirements_and_certs.any_school_decision == 1,
    1,
    classes_w_requirements_and_certs.cert_match,
)  # assume school approves TODO: Test np.nan

classes_w_requirements_and_certs["cert_match"] = np.where(
    (classes_w_requirements_and_certs.any_trade == 1)
    | (classes_w_requirements_and_certs.any_cert == 1),
    np.nan,
    classes_w_requirements_and_certs.cert_match,
)

classes_w_requirements_and_certs["cert_match"] = np.where(
    (classes_w_requirements_and_certs.any_elem == 1)
    & (classes_w_requirements_and_certs.cert_level.isin(["Elementary", "ELM"])),
    1,
    classes_w_requirements_and_certs.cert_match,
)

classes_w_requirements_and_certs["cert_match"] = np.where(
    (classes_w_requirements_and_certs.any_secondary == 1)
    & (classes_w_requirements_and_certs.cert_level.isin(["Secondary", "SEC"])),
    1,
    classes_w_requirements_and_certs.cert_match,
)

classes_w_requirements_and_certs["cert_match"] = np.where(
    (classes_w_requirements_and_certs.any_all_level == 1)
    & (classes_w_requirements_and_certs.cert_level.isin(["All Level", "ALL"])),
    1,
    classes_w_requirements_and_certs.cert_match,
)

classes_w_requirements_and_certs["cert_match"] = np.where(
    (classes_w_requirements_and_certs.any_language_grade_match == 1),
    1,
    classes_w_requirements_and_certs.cert_match,
)

classes_w_requirements_and_certs["cert_match"] = np.where(
    (classes_w_requirements_and_certs.any_cert == 1),
    1,
    classes_w_requirements_and_certs.cert_match,
)

# TODO: Edit these in another file

# any_subject_grade_match
classes_w_requirements_and_certs["cert_match"] = np.where(
    (classes_w_requirements_and_certs.any_subject_grade_match == 1),
    1,
    classes_w_requirements_and_certs.cert_match,
)
# any_grade_match
classes_w_requirements_and_certs["cert_match"] = np.where(
    (classes_w_requirements_and_certs.any_grade_match == 1),
    1,
    classes_w_requirements_and_certs.cert_match,
)
# any_esl
classes_w_requirements_and_certs["cert_match"] = np.where(
    (classes_w_requirements_and_certs.any_esl == 1),
    1,
    classes_w_requirements_and_certs.cert_match,
)
# any_sped
classes_w_requirements_and_certs["cert_match"] = np.where(
    (classes_w_requirements_and_certs.any_sped == 1),
    1,
    classes_w_requirements_and_certs.cert_match,
)
# %% Keep first match or first non-match for each teacher's class
classes_w_requirements_and_certs = classes_w_requirements_and_certs.drop_duplicates(
    subset=["teacher_id", "class_number"], keep="first"
)
classes_w_requirements_and_certs[
    [
        "DISTRICT NAME",
        "teacher_id",
        "class_number",
        "CLASS NAME",
        "CLASS TYPE NAME",
        "SUBJECT AREA NAME",
        "GRADE LEVEL NAME",
        "cert_desc",
        "_merge_requirements",
        "cert_area",
        "cert_field",
        "cert_type",
        "cert_level",
        "grade_level",
        "cert_role",
        "_cert_match",
        "cert_match",
    ]
].sample(10)
classes_w_requirements_and_certs.cert_match.value_counts()
# %%
# class 13037300
# teacher 03210D449
1 - classes_w_requirements_and_certs[
    (classes_w_requirements_and_certs.SUBJAREAX == "MATHEMATICS")
    & (classes_w_requirements_and_certs.GRADEGRP1X == "HIGH SCHOOL")
].cert_match.mean(skipna=True)

1 - classes_w_requirements_and_certs[
    (classes_w_requirements_and_certs.SUBJAREAX == "SELF-CONTAINED")
    & (classes_w_requirements_and_certs.GRADEGRP1X == "ELEMENTARY")
].cert_match.mean(skipna=True)

classes_w_requirements_and_certs[
    classes_w_requirements_and_certs.cert_match == 0
].SERVICEX.value_counts().head(10)


classes_w_requirements_and_certs["course_fte"] = pd.to_numeric(
    classes_w_requirements_and_certs.PFTE_SUM, errors="coerce"
)
classes_w_requirements_and_certs["in_field_fte"] = (
    classes_w_requirements_and_certs.cert_match
    * classes_w_requirements_and_certs.course_fte
)

classes_w_requirements_and_certs[
    (classes_w_requirements_and_certs.SUBJAREAX == "MATHEMATICS")
    & (classes_w_requirements_and_certs.GRADEGRP1X == "HIGH SCHOOL")
].in_field_fte.mean(skipna=True)
