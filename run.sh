#!/bin/bash

# data from TEA
CAMPUS=0
DISTRICT=0
TEACHERS=0
MERGE = 0


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
if [[ $MERGE = 1 ]]
then
    echo "running merge and clean"
    python merge_and_clean/01_merge_tea_and_exemptions.py
    python merge_and_clean/02_r_data.py
    echo "done"
fi

# Python Analyses
echo "running python analyses"
python analysis/00_district_eligibility_and_takeup.py
python analysis/01_table_doi_characteristics.py
python analysis/02_table_top_exemptions.py
python analysis/03_table_exemptions_by_urbanicity.py
python analysis/04_table_district_characteristics_by_exemption.py


# R analyses
chmod +x r_scripts/test.r
echo "running R analyses"
chmod +x r_scripts/00_start.r
chmod +x r_scripts/01_main.r
chmod +x r_scripts/02_htes_demographics.r
chmod +x r_scripts/03_htes_exemptions.r
chmod +x r_scripts/04_inputs.r
chmod +x r_scripts/05_main_with_matching.r
chmod +x r_scripts/06_htes_subjects.r
chmod +x r_scripts/07_effect_district.r
chmod +x r_scripts/08_effect_standardized_within_year.r
chmod +x r_scripts/09_effect_on_enrollment.r
chmod +x r_scripts/10_effect_other_subjects.r
chmod +x r_scripts/X_ever_treated.r
chmod +x r_scripts/X_ever_treated_inputs.r

# Python Formatting
echo "formatting R results"
# python analysis/05_tables_effect_on_math_and_reading.py
