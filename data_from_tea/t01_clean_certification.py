import os

import pandas as pd


from dofis import start
from dofis.data_from_tea.library import clean_tea
from dofis.data_from_tea.library import build
from dofis.data_from_tea.library import clean_teachers


pd.set_option("display.max_columns", None)

# %%

FILE_PATTERNS = {
    "yr1213": "CERTIFICATION*.TXT",
    "yr1314": "CERTIFICATION*.TXT",
    "yr1415": "CERTIFICATION_*.csv",
    "yr1516": "CERTIFICATION_*.csv",
    "yr1617": "CERTIFICATION_*.csv",
    "yr1718": "CERTIFICATION_*.csv",
    "yr1819": "STAFF_CERTIFICATION_1819*.csv",
}

YEARS = ["yr1213", "yr1314", "yr1415", "yr1516", "yr1617", "yr1718", "yr1819"]
DATA_PATH = start.DATA_PATH + "/teachers/"

VARS_TO_KEEP_YR1819 = {
    "PID_SCRAM": "teacher_id",
    "DISTRICT": "district",
    "cert_role": "role",
    "cert_type": "cert_type",
    "exp_dt": "expiration",
    "cert_level": "cert_level",
    "cert_area": "cert_area",
    "cert_field": "subject",
}

VARS_TO_KEEP_YR1516_TO_YR1718 = {
    "PERSONID_SCRAM": "teacher_id",
    "DISTRICT": "district",
    "ROLE_CREDENTIALED_FOR": "role",
    "CREDENTIAL_TYPE": "cert_type",
    "CERTIFICATE_EXPIRATION_DATE": "expiration",
    "CERTIFICATION_LEVEL": "cert_level",
    "SUBJECT_AREA": "cert_area",
    "SUBJECT": "cert_subject",
}

VARS_TO_KEEP_PRE_YR1516 = {
    "personid_SCRAM": "teacher_id",
    "DISTRICT": "district",
    "ROLE_CREDENTIALED FOR": "role",
    "CERTIFICATE EXPIRATION DATE": "expiration",
    "CREDENTIAL TYPE": "cert_type",
    "CERTIFICATION LEVEL": "cert_level",
    "SUBJECT AREA": "cert_area",
}

# %%
###
# Certification
###

for year in YEARS:

    # Files
    teacher_datapath = DATA_PATH + year
    pattern = FILE_PATTERNS[year]
    cert = build.concat_files(path=teacher_datapath, pattern=pattern)

    # Rename and keep
    if year == "yr1819":
        vars_to_keep = VARS_TO_KEEP_YR1819

    if (year > "yr1415") and (year < "yr1819"):
        vars_to_keep = VARS_TO_KEEP_YR1516_TO_YR1718

    elif year <= "yr1415":
        vars_to_keep = VARS_TO_KEEP_PRE_YR1516

    cert = clean_tea.filter_and_rename_cols(cert, vars_to_keep)

    # Keep only teachers
    cert = cert[cert.role == "Teacher"]

    # generate certification variables
    cert = clean_teachers.gen_standard_certification(
        df=cert, col="cert_type", new_var="standard"
    )

    cert = clean_teachers.gen_subject(
        df=cert,
        new_col="cert_area_math",
        area_tuple=("cert_area", "Mathematics"),
        standard_tuple=("standard", True),
    )

    cert = clean_teachers.gen_subject(
        df=cert,
        new_col="cert_area_math_high",
        area_tuple=("cert_area", "Mathematics"),
        level_tuple=("cert_level", "Secondary"),
        standard_tuple=("standard", True),
    )

    cert = clean_teachers.gen_subject(
        df=cert,
        new_col="cert_area_science",
        area_tuple=("cert_area", "Science"),
        standard_tuple=("standard", True),
    )

    cert = clean_teachers.gen_subject(
        df=cert,
        new_col="cert_area_science_high",
        area_tuple=("cert_area", "Science"),
        level_tuple=("cert_level", "Secondary"),
        standard_tuple=("standard", True),
    )

    cert = clean_teachers.gen_subject(
        df=cert,
        new_col="cert_area_cte",
        area_tuple=("cert_area", "Vocational Education"),
        standard_tuple=("standard", True),
    )
    # three teachers don't link to district number
    cert = cert[cert.district != "San Antonio"]

    ###
    # Create any certification dataframe
    ###

    # Any standard certification? (Includes alternative certification)
    teacher_yesno = cert[
        [
            "teacher_id",
            "district",
            "standard",
            "cert_area_math",
            "cert_area_math_high",
            "cert_area_science",
            "cert_area_science_high",
            "cert_area_cte",
        ]
    ]

    teacher_yesno = teacher_yesno.groupby(["teacher_id"]).max()

    # Save to CSV
    filename = "teacher_cert_" + year + ".csv"
    teacher_yesno.to_csv(os.path.join(start.DATA_PATH, "teachers", filename))
