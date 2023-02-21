#!/bin/bash

# data from TEA
CAMPUS=1
DISTRICT=1
TEACHERS=1
MERGE=1
ANALYSES=0


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
    python data_from_tea/t02_clean_classes.py
    python data_from_tea/t03_clean_and_merge_classes_with_certifications.py

fi


# merge and clean
if [[ $MERGE = 1 ]]
then
    echo "running merge and clean"
    python merge_and_clean/01_merge_tea_and_exemptions.py
    python merge_and_clean/02_r_data.py
    python merge_and_clean/02b_r_data_nevertakers.py
    python merge_and_clean/02c_r_data_district.py
    python merge_and_clean/03_r_data_alt_treatment.py
    echo "done"
fi

if [[ $ANALYSES = 1 ]]
then
# Python Analyses
# echo "running python analyses"
# python analysis/00_district_eligibility_and_takeup.py
# python analysis/01_table_doi_characteristics.py
# python analysis/02_table_top_exemptions.py
# python analysis/03_table_exemptions_by_urbanicity.py
# python analysis/04_table_district_characteristics_by_exemption.py


# R analyses
echo "running R analyses"
chmod +x r_scripts/00_start.r
chmod +x r_scripts/01_impact_inputs_main.r
chmod +x r_scripts/01_impact_inputs_secondary.r
chmod +x r_scripts/01_impact_inputs_time.r
chmod +x r_scripts/01_impacts_inputs_tot.r
chmod +x r_scripts/01b_impact_inputs_main_weights.r
chmod +x r_scripts/02_impact_outcomes_main_weighted.r
chmod +x r_scripts/02_impact_outcomes_main.r
chmod +x r_scripts/02_impact_outcomes_secondary.r
chmod +x r_scripts/03_impact_with_nevertakers.r



# Python Formatting
# echo "formatting R results"
# python analysis/figures_event_study.py
# python analysis/tables_main.py
# python analysis/tables_effect_subgroups.py
# python analysis/X_figures_demographics.py
# python analysis/X_figures_ever_treated.py
# python analysis/tables_main.py
# python analysis/X_tables_effect_standardize_within_year.py
# python analysis/X_tables_effect_subjects.py
# python analysis/X_tables_effect_with_district_as_unit.py
fi
