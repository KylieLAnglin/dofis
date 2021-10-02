import os
import fnmatch

import pandas as pd

from dofis.start import DATA_PATH

subject_year_path = os.path.join(DATA_PATH, "tea", "bysubject")

files = []
pattern = "*.csv"
for entry in os.listdir(subject_year_path):
    if fnmatch.fnmatch(entry, pattern):
        files.append(entry)
dirs = [os.path.join(subject_year_path, file) for file in files]
df_list = [
    pd.read_csv(file, sep=",", encoding="ISO-8859-1", dtype=object) for file in dirs
]
desc_long_subject = pd.concat(df_list)


desc_long_subject.to_csv((os.path.join(DATA_PATH, "tea", "desc_s_long.csv")))
