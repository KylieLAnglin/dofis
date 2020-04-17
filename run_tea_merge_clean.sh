
cd "/Users/kylie/dofis/src/data_from_tea"
python '/Users/kylie/dofis/src/data_from_tea/c01_clean_tea_data.py'
python '/Users/kylie/dofis/src/data_from_tea/c02_append_years.py'
python '/Users/kylie/dofis/src/data_from_tea/d01_clean_tea_data.py'
python '/Users/kylie/dofis/src/data_from_tea/d02_append_years.py'

cd "/Users/kylie/dofis/src/merge_and_clean"
python '/Users/kylie/dofis/src/merge_and_clean/01_merge_tea_and_exemptions.py'