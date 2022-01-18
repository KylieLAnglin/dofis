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
teacher_datapath = os.path.join(start.data_path, "teachers", year)
certs = build.concat_files(path=teacher_datapath, pattern="STAFF_CERTIFICATION*.csv")

courses = build.concat_files(path=teacher_datapath, pattern="TEACHER_CLASS*.TXT")


# %% Follow Tony Dominguez

tony_courses = courses[courses["SCRAMBLED UNIQUE ID"] == "V32650*49"]
tony_certs = certs[certs["PID_SCRAM"] == "V32650*49"]


# %%
janis_courses = courses[courses["SCRAMBLED UNIQUE ID"] == "032QV0146"]
janis_certs = certs[certs["PID_SCRAM"] == "032QV0146"]


# %%
jose_certs = certs[certs["PID_SCRAM"] == "*3034L040"]
