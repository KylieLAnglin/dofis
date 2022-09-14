# %%
import datetime
import os

import numpy as np
import pandas as pd


from dofis import start

pd.options.display.max_columns = 200


r_data = pd.read_csv(
    os.path.join(start.DATA_PATH, "clean", "r_data.csv"),
    sep=",",
)

# %%
r_data_cert_treatment = r_data
r_data_cert_treatment["group"] = np.where(
    r_data.exempt_certification == 1, r_data.group, 0
)
r_data_cert_treatment.to_csv(
    os.path.join(start.DATA_PATH, "clean", "r_data_cert.csv"),
    sep=",",
)
# %%
r_data_class_size_treatment = r_data
r_data_class_size_treatment["group"] = np.where(
    r_data.exempt_classsize == 1, r_data.group, 0
)

r_data_class_size_treatment.to_csv(
    os.path.join(start.DATA_PATH, "clean", "r_data_classize.csv"),
    sep=",",
)
