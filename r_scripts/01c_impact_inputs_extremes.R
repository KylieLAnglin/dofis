df <- read.csv(paste(data_path, "clean/r_data.csv", sep=""))


run_and_export_main(df = df, outcome = "teacher_uncertified_extreme", disag_file = "results_uncertified_disag_raw_extreme.xlsx", ag_file = "results_uncertified_ag_raw_extreme.xlsx")
run_and_export_main(df = df, outcome = "teacher_out_of_field_extreme", disag_file = "results_out_of_field_disag_raw_extreme.xlsx", ag_file = "results_out_of_field_ag_raw_extreme.xlsx")
run_and_export_main(df = df, outcome = "class_size_elem_extreme", disag_file = "results_class_size_elem_disag_raw_extreme.xlsx", ag_file = "results_class_size_elem_ag_raw_extreme.xlsx")
run_and_export_main(df = df, outcome = "stu_teach_ratio_extreme", disag_file = "results_stu_teach_ratio_disag_raw_extreme.xlsx", ag_file = "results_stu_teach_ratio_ag_raw_extreme.xlsx")
