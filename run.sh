#!/bin/bash

# data from TEA
CAMPUS=1
DISTRICT=1
TEACHERS=1


if [[ $DISTRICT = 1 ]]
then
    echo "building district data"
    python data_from_tea/d01_clean_tea_data.py
    python data_from_tea/d02_append_years.py
fi

if [[ $CAMPUS = 1 ]]
then
    echo "building campus data"
    python data_from_tea/c01_clean_tea_data.py
    pyton data_from_tea/c01_append_years.py
fi

if [[ $TEACHERS = 1 ]]
then
    echo "building teacher data"
    python data_from_tea/t01_clean_certification.py
    python data_from_tea/t02_clean_teachers.py
    python data_from_tea/t03_clean_class.py
    python data_from_tea/t03_merge_and_append.py

fi


# merge and clean
echo "running merge and clean"
python merge_and_clean/01_merge_tea_and_exemptions.py
python merge_and_clean/02_r_data.py
echo "done"

# Python Analyses
echo "running python analyses"
python analysis/01_district_eligibility_and_takeup.py
python analysis/02_table_doi_characteristics.py
python analysis/03_table_exemptions_by_urbanicity.py
python analysis/04_district_characteristics_by_exemption.py


# R analyses
echo "running R analyses"

# Python Formatting
echo "formatting R results"
python analysis/05_tables_effect_on_math_and_reading.py
