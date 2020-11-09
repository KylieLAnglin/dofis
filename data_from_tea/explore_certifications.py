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

# Files
folder = 'certification_' + year + '/'
teacher_datapath = os.path.join(start.data_path, 'tea', 'teachers', folder)

pattern = 'CERTIFICATION*.csv'  # CHANGE CHANGE CHANGE
if year == 'yr1213' or year == 'yr1314':
    pattern = 'CERTIFICATION*.TXT'

cert = build.concat_files(path=teacher_datapath, pattern=pattern)

cert = cert[cert.ROLE_CREDENTIALED_FOR == "Teacher"]

# %% Most common certification types

cert.CREDENTIAL_TYPE.value_counts()

cert = clean_teachers.gen_standard_certification(df=cert,
                                                 col='CREDENTIAL_TYPE',
                                                 new_var='standard')

cert.standard.mean()

# %% Average number of certifications by teacher?

# %%
