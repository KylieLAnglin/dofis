# %%
import pandas as pd
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

course_cert.to_csv(
    "/Users/kla21002/Dropbox/Active/dofis/data/teachers/field_requirements.csv",
    index=False,
)
# %%
