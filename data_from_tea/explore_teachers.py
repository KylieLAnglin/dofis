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
pd.set_option('display.max_columns', None)

# %%

year = 'yr1718'

folder = 'certification_' + year + '/'
teacher_datapath = os.path.join(start.data_path, 'tea', 'teachers', folder)
pattern = "TEACHER_MASTER*.TXT"

teachers = build.concat_files(path=teacher_datapath, pattern=pattern)
teachers = teachers[teachers['ROLE NAME'] == 'TEACHER']

# %%

teachers['SUBJECT AREA NAME 1'].value_counts()
# %%
