# %%
import pandas as pd
import numpy as np
import pandas as pd
from openpyxl import load_workbook
import scipy

from dofis.analysis.library import start
from dofis.analysis.library import analysis

MATH_DISAG = start.table_path + "results_math_disag_raw.xlsx"
math_disag = pd.read_excel(MATH_DISAG)

data = pd.read_csv(start.data_path + "clean/r_data_school_2020_comparison.csv")
# %%

math_disag = math_disag.rename(
    columns={
        "attgt.math.group": "cohort",
        "attgt.math.t": "year",
        "attgt.math.att": "te",
        "attgt.math.se": "se",
    }
)

math_disag["tvalue"] = math_disag.te / math_disag.se
math_disag["sig"] = np.where(abs(math_disag.tvalue) > 1.96, 1, 0)
math_disag


# %%
