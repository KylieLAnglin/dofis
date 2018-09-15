import pandas as pd
import os
from clean.library.start import data_path

tea = pd.read_csv(os.path.join(data_path, 'tea', 'desc_long.csv'), sep=",")
