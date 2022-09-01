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


def create_classes(year):

    grades_crosswalk = pd.read_excel(grades_crosswalk_path, index_col="cert_grade")

    classes = pd.read_csv(start.DATA_PATH + "teachers/classes_clean_" + year + ".csv")
    cert = pd.read_csv(start.DATA_PATH + "teachers/cert_" + year + ".csv")

    # Class teacher in certification database
    classes = classes.merge(
        cert[["teacher_id"]],
        left_on="teacher_id",
        right_on="teacher_id",
        how="left",
        indicator="_teacher_in_cert_database",
    )

    classes["teacher_in_cert_database"] = np.where(
        classes._teacher_in_cert_database == "both", 1, 0
    )

    # Class teacher certified or not according to database

    # Class teacher in field

    certified_df = cert[["teacher_id"]].drop_duplicates()

    list(grades_crosswalk.columns)
    classes.class_grade_name.value_counts()

    list(grades_crosswalk.index)
    cert_teachers.cert_grade.value_counts()

    cert_subject = cert.drop_duplicates(subset=["teacher_id", "subject"], keep="first")

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

    cert_elem = cert.sort_values(
        by=["teacher_id", "cert_elem"], ascending=False
    ).drop_duplicates(
        subset=["teacher_id"],
    )

    classes_certified_field = classes_certified_field.merge(
        cert_elem[["teacher_id", "cert_elem"]],
        left_on="teacher_id",
        right_on="teacher_id",
        how="left",
    )

    # Create grades indicator
    classes_grades_cert = classes.merge(
        cert, left_on=["teacher_id"], right_on=["teacher_id"], how="left"
    )

    in_grade = []
    for course in classes_grades_cert.index:
        class_grade = classes_grades_cert.loc[course, "class_grade_name"]
        cert_grade = classes_grades_cert.loc[course, "cert_grade"]
        if (cert_grade in list(grades_crosswalk.index)) & (
            class_grade in list(grades_crosswalk.columns)
        ):
            match = grades_crosswalk.loc[cert_grade, class_grade]
        else:
            match = np.nan
        in_grade.append(match)

    classes_grades_cert["certified_in_grade"] = in_grade
    classes_grades_cert = classes_grades_cert.sort_values(
        by=["teacher_id", "class_id", "certified_in_grade"], ascending=False
    )
    classes_grades_cert = classes_grades_cert.drop_duplicates(
        subset=["teacher_id", "class_id"]
    )
    classes_grades_cert.certified_in_grade.value_counts()
    classes_grades_cert.certified_in_grade.mean()

    classes_certified_field = classes_certified_field.merge(
        classes_grades_cert[["teacher_id", "class_id", "certified_in_grade"]],
        left_on=["teacher_id", "class_id"],
        right_on=["teacher_id", "class_id"],
    )
    # If cert_subject_area is elem or bilingual education, then change certified_in_field to 1 if certified_in_grade
    classes_certified_field["certified_in_field"] = np.where(
        (classes_certified_field.cert_elem == 1)
        & (classes_certified_field.certified_in_grade == 1),
        1,
        classes_certified_field.certified_in_field,
    )

    # Exclude other, cte, and tech classes
    classes_certified_field["certified_in_field"] = np.where(
        classes_certified_field.subject.isin(["other", "cte", "tech", "pe"]),
        np.nan,
        classes_certified_field.certified_in_field,
    )

    classes_certified_field["uncertified"] = np.where(
        classes_certified_field.certified == 0, 1, 0
    )
    classes_certified_field["uncertified"] = np.where(
        classes_certified_field.certified.isnull(),
        np.nan,
        classes_certified_field.uncertified,
    )

    classes_certified_field["certified_out_of_field"] = np.where(
        (classes_certified_field.certified == 1)
        & (classes_certified_field.certified_in_field == 0),
        1,
        0,
    )
    classes_certified_field["certified_out_of_field"] = np.where(
        (classes_certified_field.certified.isnull())
        | (classes_certified_field.certified_in_field.isnull()),
        np.nan,
        classes_certified_field.certified_out_of_field,
    )

    classes_certified_field["science_out_of_field"] = np.where(
        (classes_certified_field.subject == "science")
        & (classes_certified_field.certified_out_of_field == 1),
        1,
        0,
    )
    classes_certified_field["science_out_of_field"] = np.where(
        (classes_certified_field.certified_out_of_field.isnull())
        | (classes_certified_field.subject != "science"),
        np.nan,
        classes_certified_field.science_out_of_field,
    )

    classes_certified_field["math_out_of_field"] = np.where(
        (classes_certified_field.subject == "math")
        & (classes_certified_field.certified_out_of_field == 1),
        1,
        0,
    )
    classes_certified_field["math_out_of_field"] = np.where(
        (classes_certified_field.certified_out_of_field.isnull())
        | (classes_certified_field.subject != "math"),
        np.nan,
        classes_certified_field.math_out_of_field,
    )

    classes_certified_field = classes_certified_field[
        [
            "campus",
            "teacher_id",
            "class_name",
            "class_fte",
            "class_subject_name",
            "class_grade_name",
            "subject",
            "certified",
            "teacher_in_cert_database",
            "cert_subject",
            "cert_elem",
            "certified_in_grade",
            "certified_in_field",
            "uncertified",
            "certified_out_of_field",
            "science_out_of_field",
            "math_out_of_field",
        ]
    ]
    classes_certified_field.to_csv(
        start.DATA_PATH + "teachers/" + "classes_certs_" + year + ".csv"
    )
    return classes_certified_field


# %%

yr1213 = create_classes("yr1213")
yr1314 = create_classes("yr1314")
yr1415 = create_classes("yr1415")
yr1516 = create_classes("yr1617")
yr1718 = create_classes("yr1718")
yr1819 = create_classes("yr1819")
yr1920 = create_classes("yr1920")
yr2021 = create_classes("yr2021")
yr2122 = create_classes("yr2122")

# %%


campus_level = (
    yr1415[
        [
            "campus",
            "certified_in_field",
            "uncertified",
            "certified_out_of_field",
            "science_out_of_field",
            "math_out_of_field",
        ]
    ]
    .groupby(by=["campus"])
    .mean()
)

year = "yr2122"
classes_certified_field = create_classes("yr2122")
test = classes_certified_field.sample(10, random_state=12)

# random sample missing in field (includes other pe and cte)
test = classes_certified_field[
    classes_certified_field.certified_in_field.isnull()
].sample(10, random_state=12)

# random sample not in field (includes uncertified)
test = classes_certified_field[classes_certified_field.certified_in_field == 0].sample(
    10,
)

# random sample only out of field - random_state = 13
test = classes_certified_field[
    (classes_certified_field.certified_in_field == 0)
    & (classes_certified_field.teacher_certified == 1)
].sample(10)

# %%
