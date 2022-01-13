# %%
import pandas as pd
import os
import fnmatch
import numpy as np
import datetime

from dofis.data_from_tea.library import start
from dofis.data_from_tea.library import clean_tea
from dofis.data_from_tea.library import build
from dofis.data_from_tea.library import clean_teachers

# %%
pd.set_option("display.max_columns", None)

# %%

year = "yr1819"

teacher_datapath = start.data_path + "/teachers/" + year
# %% Teachers
pattern = "TEACHER_MASTER*.TXT"
teachers = build.concat_files(path=teacher_datapath, pattern=pattern)
teachers = teachers[teachers["ROLE NAME"] == "TEACHER"]

teachers = teachers.rename(
    columns={"DISTRICT NAME": "district", "DISTRICT CITY": "city"}
)

hamilton_teachers = teachers[teachers.district.str.contains("HAMILTON", na=False)]
hamilton_teachers = hamilton_teachers[hamilton_teachers.city == "HAMILTON"]

# %% Certification

pattern = "*CERTIFICATION*.csv"  # CHANGE CHANGE CHANGE
if year == "yr1213" or year == "yr1314":
    pattern = "CERTIFICATION*.TXT"

cert = build.concat_files(path=teacher_datapath, pattern=pattern)

cert = clean_teachers.gen_standard_certification(
    df=cert, col="cert_type", new_var="standard"
)


hamilton_certifications = cert[cert.DISTNAME.str.contains("HAMILTON")]
hamilton_certifications = hamilton_certifications[
    hamilton_certifications.city == "HAMILTON"
]

hamilton_df = hamilton_teachers.merge(
    hamilton_certifications,
    right_on="PID_SCRAM",
    left_on="SCRAMBLED UNIQUE ID",
    indicator="cert_merge",
)
# %%
uncertified = hamilton_df[hamilton_df.standard != 1]

"SCRAMBLED UNIQUE ID"
