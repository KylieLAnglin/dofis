# %%
import pandas as pd

# %%

master_data = pd.read_csv(
    "/Users/kla21002/Dropbox/Active/dofis/data/clean/master_data_district.csv"
)
# %%
df = master_data[master_data.year == 2020]
regs = [col for col in df if col.startswith("reg")]
cols = [
    "district",
    "distname",
    "distischarter",
    "doi",
    "link",
    "term_year",
    "finalize_year",
    "finalize_month",
] + regs
df = df[cols]

df.to_csv(
    "/Users/kla21002/Dropbox/Active/dofis/data/clean/doi_status_and_exemptions_update2022.csv"
)
# %%
