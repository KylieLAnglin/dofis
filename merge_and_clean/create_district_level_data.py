import os
import pandas as pd
import numpy as np
from merge_and_clean.library import start


data = pd.read_csv(os.path.join(start.data_path, 'clean', 'master_data.csv'),
            sep=",", low_memory = False)
