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


def check_in_grade(df):
    in_grade = []
    for course in df.index:
        class_grade = df.loc[course, "class_grade_name"]
        cert_grade = df.loc[course, "cert_grade"]
        if (cert_grade in list(grades_crosswalk.index)) & (
            class_grade in list(grades_crosswalk.columns)
        ):
            match = grades_crosswalk.loc[cert_grade, class_grade]
        else:
            match = np.nan
        in_grade.append(match)
    return in_grade


# %%
year = "yr1415"

years = [
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
]
for year in years:

    active_column = {
        "yr1213": "cert_active_2012",
        "yr1314": "cert_active_2013",
        "yr1415": "cert_active_2014",
        "yr1516": "cert_active_2015",
        "yr1617": "cert_active_2016",
        "yr1718": "cert_active_2017",
        "yr1819": "cert_active_2018",
        "yr1920": "cert_active_2019",
        "yr2021": "cert_active_2020",
        "yr2122": "cert_active_2021",
    }

    grades_crosswalk = pd.read_excel(grades_crosswalk_path, index_col="cert_grade")

    classes = pd.read_csv(start.DATA_PATH + "teachers/classes_clean_" + year + ".csv")
    # classes = classes.sample(15)
    cert = pd.read_csv(start.DATA_PATH + "teachers/certifications_long.csv")

    # Class teacher in certification database
    teachers_in_cert_database = (
        cert[["teacher_id"]].groupby(by=["teacher_id"]).mean().reset_index()
    )

    classes = classes.merge(
        teachers_in_cert_database[["teacher_id"]],
        left_on="teacher_id",
        right_on="teacher_id",
        how="left",
        indicator="_teacher_in_cert_database",
    )

    classes["teacher_in_cert_database"] = np.where(
        classes._teacher_in_cert_database == "both", 1, 0
    )

    # Does the teacher have an active certification *to teach* in the database?
    teachers_certified = cert[cert.certified == 1]
    teachers_certified = teachers_certified[
        teachers_certified[active_column[year]] == 1
    ]
    teachers_certified = (
        teachers_certified[["teacher_id"]]
        .groupby(by=["teacher_id"])
        .mean()
        .reset_index()
    )

    classes = classes.merge(
        teachers_certified[["teacher_id"]],
        left_on="teacher_id",
        right_on="teacher_id",
        how="left",
        indicator="_teacher_certified",
    )

    classes["teacher_certified"] = np.where(classes._teacher_certified == "both", 1, 0)
    classes.teacher_certified.mean()

    # Does the teacher have an active certification in the same subject?
    teachers_certified_fields = cert[cert.certified == 1]
    teachers_certified_fields = teachers_certified_fields[
        teachers_certified_fields[active_column[year]] == 1
    ]
    teachers_certified_fields = (
        teachers_certified_fields[["teacher_id", "subject", "cert_grade"]]
        .groupby(by=["teacher_id", "subject", "cert_grade"])
        .mean()
        .reset_index()
    )

    classes_match_subject_grade = classes.merge(
        teachers_certified_fields,
        left_on=["teacher_id", "subject"],
        right_on=["teacher_id", "subject"],
        how="left",
        indicator="_teacher_certified_in_subject",
    )  # classes_match_subject_grade now has duplicates of every class from merging to each cert

    classes_match_subject_grade["teacher_certified_in_subject"] = np.where(
        classes_match_subject_grade._teacher_certified_in_subject == "both", 1, 0
    )

    # Does the teachers have a certification in the same subject and grade?
    classes_match_subject_grade["teacher_certified_in_grade"] = check_in_grade(
        classes_match_subject_grade
    )

    classes_match_subject_grade["teacher_certified_in_subject_grade"] = np.where(
        (classes_match_subject_grade.teacher_certified_in_subject == 1)
        & (classes_match_subject_grade.teacher_certified_in_grade == 1),
        1,
        0,
    )

    classes_match_subject_grade = classes_match_subject_grade.sort_values(
        by=[
            "teacher_id",
            "class_id",
            "teacher_certified_in_subject",
            "teacher_certified_in_subject_grade",
        ],
        ascending=False,
    )

    classes_match_subject_grade = (
        classes_match_subject_grade[
            [
                "teacher_id",
                "class_id",
                "teacher_certified_in_subject",
                "teacher_certified_in_subject_grade",
            ]
        ]
        .groupby(["teacher_id", "class_id"])
        .max()
        .reset_index()
    )

    classes = classes.merge(
        classes_match_subject_grade,
        left_on=["teacher_id", "class_id"],
        right_on=["teacher_id", "class_id"],
        how="left",
    )

    # Does the teacher have an elementary certification?
    teachers_certified_elem = cert[cert.certified == 1]
    teachers_certified_elem = teachers_certified_elem[
        teachers_certified_elem[active_column[year]] == 1
    ]
    teachers_certified_elem = teachers_certified_elem[
        teachers_certified_elem.cert_elem == 1
    ]

    teachers_certified_elem = teachers_certified_elem[
        ["teacher_id", "cert_elem", "cert_grade"]
    ].drop_duplicates(keep="first")

    classes_match_elem_grade = classes.merge(
        teachers_certified_elem,
        left_on=["teacher_id"],
        right_on="teacher_id",
        how="left",
        indicator="_teacher_certified_elementary",
    )

    classes_match_elem_grade["teacher_certified_elementary"] = np.where(
        classes_match_elem_grade._teacher_certified_elementary == "both", 1, 0
    )

    # TODO: Handle elementary certification which doesn't always match subject

    classes_match_elem_grade[
        "teacher_certified_in_elementary_and_grade"
    ] = check_in_grade(classes_match_elem_grade)

    classes_match_elem_grade = (
        classes_match_elem_grade[
            [
                "teacher_id",
                "class_id",
                "teacher_certified_elementary",
                "teacher_certified_in_elementary_and_grade",
            ]
        ]
        .groupby(by=["teacher_id", "class_id"])
        .max()
    )

    classes = classes.merge(
        classes_match_elem_grade,
        left_on=["teacher_id", "class_id"],
        right_on=["teacher_id", "class_id"],
    )

    classes["teacher_certified_in_subject"] = np.where(
        (classes.teacher_certified_in_subject == 0)
        & (classes.teacher_certified_in_elementary_and_grade == 1),
        1,
        classes.teacher_certified_in_subject,
    )

    # Exclude other, cte, and tech classes
    classes["teacher_certified_in_subject"] = np.where(
        classes.subject.isin(["other", "cte", "tech", "pe"]),
        np.nan,
        classes.teacher_certified_in_subject,
    )

    # Create negative indicators
    classes["teacher_uncertified"] = np.where(classes.teacher_certified == 1, 1, 0)

    classes["teacher_out_of_field"] = np.where(
        classes.teacher_certified_in_subject == 0, 1, 0
    )
    classes["teacher_out_of_field"] = np.where(
        classes.teacher_certified_in_subject.isnull(),
        np.nan,
        classes.teacher_out_of_field,
    )
    classes["teacher_out_of_field"] = np.where(
        classes.teacher_certified == 0, np.nan, classes.teacher_out_of_field
    )

    # TODO: Decide unit - teacher or class? If teacher, use fte.
    # Group to teacher level, how to weight by fte?
    classes["class_fte"] = pd.to_numeric(classes.class_fte, errors="coerce")
    classes["teacher_out_of_field_fte"] = (
        classes.teacher_out_of_field * classes.class_fte
    )

    teachers = (
        classes[
            [
                "district",
                "campus",
                "teacher_id",
                "teacher_certified",
                "teacher_out_of_field_fte",
            ]
        ]
        .groupby(["district", "campus", "teacher_id"])
        .agg(
            {
                "teacher_certified": "max",
                "teacher_out_of_field_fte": "sum",
            }
        )
    ).reset_index()

    teachers["teacher_uncertified"] = np.where(teachers.teacher_certified == 0, 1, 0)
    teachers["teacher_uncertified"] = np.where(
        teachers.teacher_certified.isnull(), np.nan, teachers.teacher_uncertified
    )

    # Groupby to campus level with means of teacher_certified, teacher_out_of_field_fte
    schools = (
        teachers[
            [
                "district",
                "campus",
                "teacher_certified",
                "teacher_uncertified",
                "teacher_out_of_field_fte",
            ]
        ]
        .groupby(by=["district", "campus"])
        .mean()
    ).reset_index()

    # Percent of science classes within a school that are taught by an out of field teacher
    science_classes = classes[classes.subject == "science"]
    campus_science = (
        science_classes[["campus", "teacher_certified", "teacher_out_of_field"]]
        .groupby("campus")
        .mean()
    ).reset_index()
    campus_science = campus_science.rename(
        columns={
            "teacher_certified": "science_teachers_certified",
            "teacher_out_of_field": "science_teachers_out_of_field",
        }
    )

    math_classes = classes[classes.subject == "math"]
    campus_math = (
        math_classes[["campus", "teacher_certified", "teacher_out_of_field"]]
        .groupby("campus")
        .mean()
    ).reset_index()
    campus_math = campus_math.rename(
        columns={
            "teacher_certified": "math_teachers_certified",
            "teacher_out_of_field": "math_teachers_out_of_field",
        }
    )

    schools = schools.merge(
        campus_science, left_on="campus", right_on="campus", how="left"
    )
    schools = schools.merge(
        campus_math, left_on="campus", right_on="campus", how="left"
    )

    schools.to_csv(
        start.DATA_PATH + "campus_certification_" + year + ".csv", index=False
    )


# %%
# TODO: Import and append
appended_data = []
for year in years:
    data = pd.read_csv(start.DATA_PATH + "campus_certification_" + year + ".csv")
    data["year"] = year
    appended_data.append(data)

appended_data = pd.concat(appended_data)

# # # If cert_subject_area is elem or bilingual education, then change certified_in_field to 1 if certified_in_grade
# # classes_certified_field["certified_in_field"] = np.where(
# #     (classes_certified_field.cert_elem == 1)
# #     & (classes_certified_field.certified_in_grade == 1),
# #     1,
# #     classes_certified_field.certified_in_field,
# # )

# %%
