import pandas as pd
import os
from data_from_tea.library.start import data_path
import fnmatch

subject_year_path = os.path.join(data_path, 'tea', 'bysubject')

files = []
pattern = "*.csv"
for entry in os.listdir(subject_year_path):
    if fnmatch.fnmatch(entry, pattern):
        files.append(entry)
dirs = [os.path.join(subject_year_path, file) for file in files]
df_list = [pd.read_csv(file, sep=",", encoding="ISO-8859-1", dtype=object) for file in dirs]
desc_long_subject = pd.concat(df_list)


desc_long_subject.to_csv((os.path.join(data_path, 'tea', 'desc_s_long.csv')))

