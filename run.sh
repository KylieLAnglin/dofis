#!/bin/bash

# data from TEA
CAMPUS=1
DISTRICT=1
TEACHERS=1
MERGE=1
ANALYSES=1


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
    python data_from_tea/c01_append_years.py
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

if [[ $ANALYSES = 1 ]]
then
# Python Analyses
echo "running python analyses"
python analysis/00_district_eligibility_and_takeup.py
python analysis/01_table_doi_characteristics.py
python analysis/02_table_top_exemptions.py
python analysis/03_table_exemptions_by_urbanicity.py
python analysis/04_table_district_characteristics_by_exemption.py


# R analyses
echo "running R analyses"
chmod +x r_scripts/00_start.r
chmod +x r_scripts/01_main.r
chmod +x r_scripts/02_htes_demographics.r
chmod +x r_scripts/03_htes_exemptions.r
chmod +x r_scripts/X_effect_bio_and_us.r
chmod +x r_scripts/X_effect_district.r
chmod +x r_scripts/X_effect_ever_treated_inputs.r
chmod +x r_scripts/X_effect_ever_treated.r
chmod +x r_scripts/X_effect_enrollment.r
chmod +x r_scripts/X_standardized_within_year.r
chmod +x r_scripts/X_effect_with_matching.r
chmod +x r_scripts/X_htes_subjects.r


# Python Formatting
echo "formatting R results"
python analysis/figures_event_study.py
python analysis/tables_main.py
python analysis/tables_effect_subgroups.py
python analysis/X_figures_demographics.py
python analysis/X_figures_ever_treated.py
python analysis/tables_main.py
python analysis/X_tables_effect_standardize_within_year.py
python analysis/X_tables_effect_subjects.py
python analysis/X_tables_effect_with_district_as_unit.py
fi
