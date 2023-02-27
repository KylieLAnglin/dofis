#!/bin/bash

# data from TEA
CAMPUS=0
DISTRICT=0
TEACHERS=0
MERGE=0
ANALYSES=1
FORMATTING=0


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
    python data_from_tea/c02_append_years.py
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
chmod +x r_scripts/01a_impact_inputs_main.r
chmod +x r_scripts/01b_impact_inputs_secondary.r
chmod +x r_scripts/01c_impact_inputs_time.r
chmod +x r_scripts/01d_impacts_inputs_tot.r
chmod +x r_scripts/01e_impact_inputs_main_weights.r
chmod +x r_scripts/01f_impact_inputs_extremes.r
chmod +x r_scripts/02a_impact_outcomes_main.r
chmod +x r_scripts/02b_impact_outcomes_secondary.r
chmod +x r_scripts/02c_impact_outcomes_main_weighted.r
chmod +x r_scripts/03_impact_with_nevertakers.r
chmod +x r_scripts/X_effect_on_enrollment.r

r_scripts/00_start.r
# chmod +x r_scripts/01a_impact_inputs_main.r
# chmod +x r_scripts/01b_impact_inputs_secondary.r
# chmod +x r_scripts/01c_impact_inputs_time.r
# chmod +x r_scripts/01d_impacts_inputs_tot.r
# chmod +x r_scripts/01e_impact_inputs_main_weights.r
# chmod +x r_scripts/01f_impact_inputs_extremes.r
# chmod +x r_scripts/02a_impact_outcomes_main.r
# chmod +x r_scripts/02b_impact_outcomes_secondary.r
# chmod +x r_scripts/02c_impact_outcomes_main_weighted.r
# chmod +x r_scripts/03_impact_with_nevertakers.r
# chmod +x r_scripts/X_effect_on_enrollment.r
# chmod +x r_scripts/04_Table3.r

echo "finished R analyses"

fi

if [[ $FORMATTING = 1 ]]
then
# Python Formatting
echo "formatting R results"
python analysis/Table1_exemptions.py
python analysis/Table1b_exemptions_w_proportion_students.py
python analysis/Table2_proportion_districts_exempting_by_urbanicity.py
python analysis/Table3_aggregate_impacts.py

python analysis/Figure3_descriptive_main_inputs.py
python analysis/Figure4_descriptive_secondary_inputs.py
python analysis/Figure5_descriptive_inputs_time.py
python analysis/Figure6_impact_inputs_main.py
python analysis/Figure7_impact_inputs_secondary.py
python analysis/Figure8_impact_inputs_time.py
python analysis/Figure9_descriptive_main_outcomes.py
python analysis/Figure10_impact_main_outcomes.py
python analysis/Figure3_descriptive_main_inputs.py

python analysis/AppendixA_FigureA1_cohort_trends_inputs.py
python analysis/AppendixA_FigureA2_cohort_trends_outcomes.py
python analysis/AppendixA_TableA1_district_cohort_characteristics.py
python analysis/AppendixA_TableA2_district_sample_sizes.py
python analysis/AppendixA_TableA3_school_sample_sizes.py
python analysis/AppendixA_TableA4_exempter_characteristics.py

python analysis/AppendixC_FigureC1_input_boxplots.py
python analysis/AppendixC_FigureC2_descriptive_main_outcomes_post_covid.py

python analysis/AppendixD_FigureD1_impact_inputs_exemption_as_treatment.py
python analysis/AppendixD_FigureD2_inputs_w_nevertakers.py
python analysis/AppendixD_FigureD3_outcomes_w_nevertakers.py
python analysis/AppendixD_FigureD4_impact_main_inputs_weighted.py
python analysis/AppendixD_FigureD5_impact_main_outcomes_weighted.py
python analysis/AppendixD_FigureD6_impact_on_enrollment.py
python analysis/AppendixD_TableD2_impact_subjects.py

python analysis/X_big_changes.py
python analysis/X_tables_effect_standardize_within_year.py
python analysis/X_big_changes.py
python analysis/X_tables_effects_with_district_as_unit.py

fi
