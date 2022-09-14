###
# Main inputs
###
df <- read.csv(paste(data_path, "clean/r_data.csv", sep=""))

run_and_export_main(df = df, outcome = "teacher_uncertified", disag_file = "results_uncertified_disag_raw.xlsx", ag_file = "results_uncertified_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "teacher_out_of_field_fte", disag_file = "results_out_of_field_disag_raw.xlsx", ag_file = "results_uncertified_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "class_size_elem", disag_file = "results_class_size_elem_disag_raw.xlsx", ag_file = "results_class_size_elem_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "stu_teach_ratio", disag_file = "results_stu_teach_ratio_disag_raw.xlsx", ag_file = "results_stu_teach_ratio_ag_raw.xlsx")

# Impact on number of teachers, number of new teachers, average teacher tenure, average teacher experience
run_and_export_main(df = df, outcome = "teachers_num", disag_file = "results_teachers_num_disag_raw.xlsx", ag_file = "results_teachers_num_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "teachers_new_num", disag_file = "results_teachers_new_num_disag_raw.xlsx", ag_file = "results_teachers_new_num_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "teachers_tenure_ave", disag_file = "results_teacher_tenure_disag_raw.xlsx", ag_file = "results_teacher_tenure_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "teachers_turnover_ratio_d", disag_file = "results_teacher_turnover_disag_raw.xlsx", ag_file = "results_teacher_turnover_ag_raw.xlsx")

