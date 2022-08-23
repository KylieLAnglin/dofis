# %%
import pandas as pd
import numpy as np
from dofis import start

cert_licences = pd.read_excel(
    "/Users/kla21002/Dropbox/Active/dofis/RE__DOI_Data from Jeremy/Cert_licenses.xlsx"
)
cert_licences = cert_licences.rename(
    columns={"cert_license_id": "cert_id"}
)  # This is a unique certification code for each subject area, grade level, and administrative code timing (e.g., 2000 standards)
cert_licences = cert_licences[["cert_id", "cert_desc"]]
# %%
course_requirements = pd.read_excel(
    "/Users/kla21002/Dropbox/Active/dofis/RE__DOI_Data from Jeremy/Serv_cert_rqmts.xlsx"
)
course_requirements = course_requirements.rename(
    columns={"cert_req": "cert_id", "service": "class_number"}
)
course_requirements = course_requirements[["cert_id", "class_number"]]


# %%
course_cert = course_requirements.merge(
    cert_licences, how="left", on=["cert_id"], indicator=True
)


# %%
course_cert["cert_any_desc"] = np.where(
    (course_cert.cert_desc.str.contains("Any "))
    | course_cert.cert_desc.str.contains("any "),
    1,
    0,
)
course_cert["any_trade"] = np.where(
    course_cert.cert_desc
    == "Any Trades and Industrial Education or Vocational Trades and Industry certificate",
    1,
    0,
)
course_cert["any_elem"] = np.where(
    course_cert.cert_desc == "Any elementary certificate", 1, 0
)
course_cert["any_secondary"] = np.where(
    course_cert.cert_desc == "Any secondary certificate", 1, 0
)
course_cert["any_all_level"] = np.where(
    course_cert.cert_desc == "Any all-level certificate", 1, 0
)
course_cert["any_school_decision"] = np.where(
    course_cert.cert_desc.str.startswith(
        "Any teacher certificate appropriate for grade level of assignment or appropriate qualifications as determined by the school"
    ),
    1,
    0,
)
course_cert["any_language_grade_match"] = np.where(
    course_cert.cert_desc
    == "Any teacher certificate in the appropriate language and grade level of assignment",
    1,
    0,
)
course_cert["any_cte"] = np.where(
    (
        course_cert.cert_desc
        == "Any vocational or career and technical education (CTE) classroom teaching certificate"
    )
    | (
        course_cert.cert_desc
        == "Any vocational or career and technical education (CTE) classroom teaching certificate with a bachelor’s degree and 18 semester credit hours in any combination of sciences"
    ),
    1,
    0,
)
course_cert["any_subject_grade_match"] = np.where(
    course_cert.cert_desc
    == "Any valid classroom teaching certificate appropriate for the grade level and subject area",
    1,
    0,
)
course_cert["any_grade_match"] = np.where(
    course_cert.cert_desc
    == "Any teacher certificate appropriate for grade level of assignment",
    1,
    0,
)

course_cert["any_cert"] = np.where(
    course_cert.cert_desc == "Any valid classroom teacher or administrator certificate",
    1,
    0,
)
course_cert["any_esl"] = np.where(course_cert.cert_desc == "Any ESL certificate", 1, 0)
course_cert["any_sped"] = np.where(
    course_cert.cert_desc == "Any Special Education certificate", 1, 0
)
# %%
course_cert.to_csv(
    "/Users/kla21002/Dropbox/Active/dofis/data/teachers/field_requirements.csv",
    index=False,
)
# %%
