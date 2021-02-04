import os

import numpy as np
import pandas as pd

from library import start

IF_TEACHER_NOT_IN_CERT_DF_SET_AS = "missing"
# SECONDARY_VALUES = ["HIGH SCHOOL", "MIDDLE SCHOOL", "JUNIOR HIGH SCHOOL"]
SECONDARY_VALUES = ["HIGH SCHOOL"]
YEARS = ["yr1213", "yr1314", "yr1415", "yr1516", "yr1617", "yr1718", "yr1819"]

# %%

campus_df = []
for year in YEARS:

    filename = "teacher_cert_" + year + ".csv"
    certification = pd.read_csv(os.path.join(start.data_path, "teachers", filename))
    certification = certification.rename(columns={"district": "district_cert"})

    filename = "teachers_" + year + ".csv"
    teachers = pd.read_csv(os.path.join(start.data_path, "teachers", filename))

    filename = "classes_" + year + ".csv"
    classes = pd.read_csv(os.path.join(start.data_path, "teachers", filename))

    teachers = teachers.merge(
        certification, how="left", on="teacher_id", indicator="cert_merge"
    )

    teachers = teachers.merge(classes, how="left", on=["teacher_id", "campus"])

    if IF_TEACHER_NOT_IN_CERT_DF_SET_AS == "uncertified":
        for var in [
            "standard",
            "cert_area_math",
            "cert_area_math_high",
            "cert_area_science",
            "cert_area_science_high",
        ]:
            teachers[var] = np.where(
                teachers.cert_merge == "left_only", 0, teachers[var]
            )

    # Secondary Math

    teachers["secondary"] = np.where(
        (teachers.camp_grade_group.isin(SECONDARY_VALUES)), True, False
    )

    teachers["secondary_math_teacher"] = np.where(
        (teachers.secondary & teachers.math), True, False
    )

    teachers["certified_secondary_math_teacher"] = np.where(
        (teachers.secondary_math_teacher & teachers.cert_area_math),
        True,
        False,
    )

    teachers["uncertified_secondary_math_teacher"] = np.where(
        (teachers.secondary_math_teacher) & (teachers.standard == False),
        True,
        False,
    )

    teachers["outoffield_secondary_math_teacher"] = np.where(
        (teachers.secondary_math_teacher)
        & (teachers.standard)
        & (teachers.cert_area_math == False),
        True,
        False,
    )

    # Secondary Science
    teachers["secondary_science_teacher"] = np.where(
        (teachers.secondary & teachers.science), True, False
    )

    teachers["certified_secondary_science_teacher"] = np.where(
        (teachers.secondary_science_teacher & teachers.cert_area_science),
        True,
        False,
    )

    teachers["uncertified_secondary_science_teacher"] = np.where(
        (teachers.secondary_science_teacher) & (teachers.standard == False),
        True,
        False,
    )

    teachers["outoffield_secondary_science_teacher"] = np.where(
        (teachers.secondary_science_teacher)
        & (teachers.standard)
        & (teachers.cert_area_science == False),
        True,
        False,
    )

    # Standard certification
    teachers["teachers"] = 1
    teachers["teachers_certified"] = teachers.standard
    teachers["teachers_uncertified"] = np.where(teachers.standard == False, True, False)

    # Create school counts
    campus = (
        teachers[
            [
                "campus",
                "teachers",
                "teachers_certified",
                "teachers_uncertified",
                "secondary_math_teacher",
                "certified_secondary_math_teacher",
                "uncertified_secondary_math_teacher",
                "outoffield_secondary_math_teacher",
                "secondary_science_teacher",
                "certified_secondary_science_teacher",
                "uncertified_secondary_science_teacher",
                "outoffield_secondary_science_teacher",
            ]
        ]
        .groupby(["campus"])
        .sum()
    )

    # Add year variable
    years = {
        "yr1112": 2012,
        "yr1213": 2013,
        "yr1314": 2014,
        "yr1415": 2015,
        "yr1516": 2016,
        "yr1617": 2017,
        "yr1718": 2018,
        "yr1819": 2019,
    }
    campus["year"] = years[year]

    campus_df.append(campus)
    # Save
    # filename = "campus_cert_" + year + ".csv"
    # campus.to_csv(os.path.join(start.data_path, "teachers", filename))


###
#   Append
###
certification_rates_long = pd.concat(campus_df)

certification_rates_long.to_csv(
    (os.path.join(start.data_path, "tea", "certification_rates_long.csv"))
)