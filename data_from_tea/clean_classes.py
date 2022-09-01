# %%
import pandas as pd
import numpy as np

from dofis import start
from dofis.data_from_tea.library import build

# %%

classes_crosswalk_path = start.DATA_PATH + "teachers/crosswalk_classes.xlsx"
certification_crosswalk_path = start.DATA_PATH + "teachers/crosswalk_certification.xlsx"
certification_types_crosswalk_path = (
    start.DATA_PATH + "teachers/crosswalk_certification_types.xlsx"
)
subject_areas_crosswalk_path = start.DATA_PATH + "teachers/crosswalk_subject_areas.xlsx"
grades_crosswalk_path = start.DATA_PATH + "teachers/crosswalk_grades.xlsx"


# %%

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
    classes_crosswalk = pd.read_excel(classes_crosswalk_path, index_col="year")

    subject_areas_crosswalk = pd.read_excel(subject_areas_crosswalk_path)
    subject_areas_crosswalk = dict(
        zip(
            subject_areas_crosswalk.original_subject_area,
            subject_areas_crosswalk.new_subject_area,
        )
    )

    grades_crosswalk = pd.read_excel(grades_crosswalk_path, index_col="cert_grade")

    teacher_datapath = start.DATA_PATH + "teachers/" + year + "/"

    classes_crosswalk = classes_crosswalk.loc[year]
    classes_crosswalk = classes_crosswalk.to_dict()
    classes_crosswalk_invert = {v: k for k, v in classes_crosswalk.items()}

    classes = build.concat_files(
        path=teacher_datapath, pattern=classes_crosswalk["filepattern"]
    )
    classes = classes.rename(columns=classes_crosswalk_invert)

    classes = classes.loc[:, classes.columns.isin(list(classes_crosswalk.keys()))]

    subject_areas_crosswalk
    classes.class_subject_area_name.value_counts()
    classes["subject"] = classes["class_subject_area_name"].map(subject_areas_crosswalk)

    classes.to_csv(start.DATA_PATH + "teachers/classes_clean_" + year + ".csv")
