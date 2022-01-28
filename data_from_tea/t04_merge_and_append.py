# %%
import os

import numpy as np
import pandas as pd

from dofis import start

IF_TEACHER_NOT_IN_CERT_DF_SET_AS = "missing"
# SECONDARY_VALUES = ["HIGH SCHOOL", "MIDDLE SCHOOL", "JUNIOR HIGH SCHOOL"]
SECONDARY_VALUES = ["HIGH SCHOOL"]
YEARS = ["yr1213", "yr1314", "yr1415", "yr1516", "yr1617", "yr1718", "yr1819"]

# %%

campus_df = []
for year in YEARS:

    filename = "teacher_cert_" + year + ".csv"
    certification = pd.read_csv(os.path.join(start.DATA_PATH, "teachers", filename))
    certification = certification.rename(columns={"district": "district_cert"})

    filename = "teachers_" + year + ".csv"
    teachers = pd.read_csv(os.path.join(start.DATA_PATH, "teachers", filename))

    filename = "classes_" + year + ".csv"
    classes = pd.read_csv(os.path.join(start.DATA_PATH, "teachers", filename))

    teachers = teachers.merge(
        certification, how="left", on="teacher_id", indicator="cert_merge"
    )

    teachers = teachers.merge(classes, how="left", on=["teacher_id", "campus"])

    if IF_TEACHER_NOT_IN_CERT_DF_SET_AS == "uncertified":
        certification_variables = list(
            teachers.filter(like="cert_area", axis=1).columns
        )
        certification_variables = ["standard"] + certification_variables
        for var in certification_variables:
            teachers[var] = np.where(
                teachers.cert_merge == "left_only", 0, teachers[var]
            )

    # Secondary Math

    teachers["teacher_secondary"] = np.where(teachers.teaches_high == True, True, False)

    teachers["teacher_secondary_math"] = np.where(
        ((teachers.teacher_secondary) & (teachers.teaches_math)), True, False
    )

    teachers["teacher_secondary_math"] = np.where(
        teachers.teaches_math_high == True, True, False
    )
    teachers["teacher_secondary_math_certified"] = np.where(
        (teachers.teacher_secondary_math & teachers.cert_area_math),
        True,
        False,
    )

    teachers["teacher_secondary_math_uncertified"] = np.where(
        (teachers.teacher_secondary_math) & (teachers.standard == False),
        True,
        False,
    )

    teachers["teacher_secondary_math_outoffield"] = np.where(
        (teachers.teacher_secondary_math)
        & (teachers.standard)
        & (teachers.cert_area_math == False),
        True,
        False,
    )

    # Secondary Science
    teachers["teacher_secondary_science"] = np.where(
        (teachers.teacher_secondary & teachers.teaches_science), True, False
    )

    teachers["teacher_secondary_science_certified"] = np.where(
        (teachers.teacher_secondary_science & teachers.cert_area_science),
        True,
        False,
    )

    teachers["teacher_secondary_science_uncertified"] = np.where(
        (teachers.teacher_secondary_science) & (teachers.standard == False),
        True,
        False,
    )

    teachers["teacher_secondary_science_outoffield"] = np.where(
        (teachers.teacher_secondary_science)
        & (teachers.standard)
        & (teachers.cert_area_science == False),
        True,
        False,
    )

    # CTE
    teachers["teacher_secondary_cte"] = np.where(
        (teachers.teacher_secondary & teachers.teaches_cte), True, False
    )

    teachers["teacher_secondary_cte_certified"] = np.where(
        (teachers.teacher_secondary_cte & teachers.cert_area_cte),
        True,
        False,
    )

    teachers["teacher_secondary_cte_uncertified"] = np.where(
        (teachers.teacher_secondary_cte) & (teachers.standard == False),
        True,
        False,
    )

    teachers["teacher_secondary_cte_outoffield"] = np.where(
        (teachers.teacher_secondary_cte)
        & (teachers.standard)
        & (teachers.cert_area_cte == False),
        True,
        False,
    )

    # Standard certification
    teachers["teachers"] = 1
    teachers["teacher_certified"] = teachers.standard
    teachers["teacher_uncertified"] = np.where(teachers.standard == False, True, False)

    relevant_variables = list(teachers.filter(like="teacher", axis=1).columns)
    relevant_variables = ["campus"] + relevant_variables

    # Create school counts
    campus = teachers[relevant_variables].groupby(["campus"]).sum()

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
    # campus.to_csv(os.path.join(start.DATA_PATH, "teachers", filename))


###
#   Append
###
certification_rates_long = pd.concat(campus_df)

certification_rates_long.to_csv(
    (os.path.join(start.DATA_PATH, "tea", "certification_rates_long.csv"))
)
