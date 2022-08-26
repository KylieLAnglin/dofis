# %%
import pandas as pd
import numpy as np

from dofis import start
from dofis.data_from_tea.library import build

year = "yr1819"

teacher_datapath = start.DATA_PATH + "teachers/" + year + "/"

classes_crosswalk_path = start.DATA_PATH + "teachers/crosswalk_classes.xlsx"
classes_crosswalk = pd.read_excel(classes_crosswalk_path, index_col="year")
classes_crosswalk = classes_crosswalk.loc[year]
classes_crosswalk = classes_crosswalk.to_dict()
classes_crosswalk_invert = {v: k for k, v in classes_crosswalk.items()}

certification_crosswalk_path = start.DATA_PATH + "teachers/crosswalk_certification.xlsx"
certification_crosswalk = pd.read_excel(certification_crosswalk_path, index_col="year")
certification_crosswalk = certification_crosswalk.loc[year]
certification_crosswalk = certification_crosswalk.to_dict()
certification_crosswalk_invert = {v: k for k, v in certification_crosswalk.items()}

certification_types_crosswalk_path = (
    start.DATA_PATH + "teachers/crosswalk_certification_types.xlsx"
)
certification_types_crosswalk = pd.read_excel(certification_types_crosswalk_path)
certification_types_crosswalk = dict(
    zip(
        certification_types_crosswalk.cert_type, certification_types_crosswalk.certified
    )
)

subject_areas_crosswalk_path = start.DATA_PATH + "teachers/crosswalk_subject_areas.xlsx"
subject_areas_crosswalk = pd.read_excel(subject_areas_crosswalk_path)
subject_areas_crosswalk = dict(
    zip(
        subject_areas_crosswalk.original_subject_area,
        subject_areas_crosswalk.new_subject_area,
    )
)

grades_crosswalk_path = start.DATA_PATH + "teachers/crosswalk_grades.xlsx"
grades_crosswalk = pd.read_excel(grades_crosswalk_path, index_col="cert_grade")

# %%
classes = build.concat_files(
    path=teacher_datapath, pattern=classes_crosswalk["filepattern"]
)
classes = classes.rename(columns=classes_crosswalk_invert)
classes = classes.loc[:, classes.columns.isin(list(classes_crosswalk.keys()))]

# %%

pattern = "STAFF_CERTIFICATION_1819*.csv"
cert = build.concat_files(path=teacher_datapath, pattern=pattern)
cert = cert.rename(columns=certification_crosswalk_invert)
cert = cert.loc[:, cert.columns.isin(list(certification_crosswalk.keys()))]

cert["certified"] = cert["cert_type"].map(certification_types_crosswalk)
cert_teachers = cert[cert.cert_role == "Teacher"]
cert_teachers = cert[cert.certified == 1]


# %% Create certified indicator

certified_df = cert_teachers[["teacher_id"]].drop_duplicates()

# %% Create certified indicator
classes_certified = classes.merge(
    certified_df,
    left_on="teacher_id",
    right_on="teacher_id",
    how="left",
    indicator="_teacher_certified",
)

classes_certified["teacher_certified"] = np.where(
    classes_certified._teacher_certified == "both", 1, 0
)

# %% Create in field indicator
classes_certified["subject"] = classes_certified["class_subject_area_name"].map(
    subject_areas_crosswalk
)

cert_teachers["subject"] = cert_teachers["cert_subject_area"].map(
    subject_areas_crosswalk
)

cert_subject = cert_teachers.drop_duplicates(
    subset=["teacher_id", "subject"], keep="first"
)

classes_certified_field = classes_certified.merge(
    cert_subject,
    left_on=["teacher_id", "subject"],
    right_on=["teacher_id", "subject"],
    how="left",
    indicator="_in_field",
)
classes_certified_field["certified_in_field"] = np.where(
    classes_certified_field._in_field == "both", 1, 0
)


# %% Create grades indicator
classes_grades_cert = classes.merge(
    cert_teachers, left_on=["teacher_id"], right_on=["teacher_id"], how="left"
)

# %%
in_field = []
for course in classes_grades_cert.index:
    class_grade = classes_grades_cert.loc[course, "class_grade_name"]
    cert_grade = classes_grades_cert.loc[course, "cert_grade"]
    if (cert_grade in list(grades_crosswalk.index)) & (
        class_grade in list(grades_crosswalk.columns)
    ):
        match = grades_crosswalk.loc[cert_grade, class_grade]
    else:
        match = np.nan
    in_field.append(match)

classes_grades_cert["certified_in_grade"] = in_field
classes_grades_cert = classes_grades_cert.sort_values(
    by=["teacher_id", "class_id", "certified_in_grade"], ascending=False
)
classes_grades_cert = classes_grades_cert.drop_duplicates(
    subset=["teacher_id", "class_id"]
)
classes_grades_cert.certified_in_grade.value_counts()
classes_grades_cert.certified_in_grade.mean()
# %%
# If cert_subject_area is elem, then change certified_in_field to 1 if certified_in_grade
# Change certified_in_field to nan if cert_subject_area is elem and certified_in_grade is nan
