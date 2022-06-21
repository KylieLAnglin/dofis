import pandas as pd
import os
from dofis.start import DATA_PATH


desc_c_yr1112 = pd.read_csv((os.path.join(DATA_PATH, "tea", "desc_c_yr1112.csv")))
desc_c_yr1213 = pd.read_csv((os.path.join(DATA_PATH, "tea", "desc_c_yr1213.csv")))
desc_c_yr1314 = pd.read_csv((os.path.join(DATA_PATH, "tea", "desc_c_yr1314.csv")))
desc_c_yr1415 = pd.read_csv((os.path.join(DATA_PATH, "tea", "desc_c_yr1415.csv")))
desc_c_yr1516 = pd.read_csv((os.path.join(DATA_PATH, "tea", "desc_c_yr1516.csv")))
desc_c_yr1617 = pd.read_csv((os.path.join(DATA_PATH, "tea", "desc_c_yr1617.csv")))
desc_c_yr1718 = pd.read_csv((os.path.join(DATA_PATH, "tea", "desc_c_yr1718.csv")))
desc_c_yr1819 = pd.read_csv((os.path.join(DATA_PATH, "tea", "desc_c_yr1819.csv")))
desc_c_yr1920 = pd.read_csv((os.path.join(DATA_PATH, "tea", "desc_c_yr1920.csv")))
desc_c_yr2021 = pd.read_csv((os.path.join(DATA_PATH, "tea", "desc_c_yr2021.csv")))

desc_long = pd.concat(
    [
        desc_c_yr1112,
        desc_c_yr1213,
        desc_c_yr1314,
        desc_c_yr1415,
        desc_c_yr1516,
        desc_c_yr1617,
        desc_c_yr1718,
        desc_c_yr1819,
        desc_c_yr1920,
        desc_c_yr2021,
    ],
    sort=True,
)

desc_long.to_csv((os.path.join(DATA_PATH, "tea", "desc_c_long.csv")))
