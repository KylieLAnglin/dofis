###
# Main inputs
###
df <- read.csv(paste(data_path, "clean/r_data.csv", sep=""))

run_and_export_main(df = df, outcome = "teacher_uncertified", disag_file = "results_uncertified_disag_raw_average.xlsx", ag_file = "results_uncertified_ag_raw_average.xlsx")
run_and_export_main(df = df, outcome = "teacher_out_of_field_fte", disag_file = "results_out_of_field_disag_raw_average.xlsx", ag_file = "results_uncertified_ag_raw_average.xlsx")
run_and_export_main(df = df, outcome = "class_size_elem", disag_file = "results_class_size_elem_disag_raw_average.xlsx", ag_file = "results_class_size_elem_ag_raw_average.xlsx")
run_and_export_main(df = df, outcome = "stu_teach_ratio", disag_file = "results_stu_teach_ratio_disag_raw_average.xlsx", ag_file = "results_stu_teach_ratio_ag_raw_average.xlsx")

# Rural
rural <- df[ which(df$pre_rural == 1),]
run_and_export_main(df = df, outcome = "teacher_uncertified", disag_file = "results_uncertified_disag_raw_rural.xlsx", ag_file = "results_uncertified_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "teacher_out_of_field_fte", disag_file = "results_out_of_field_disag_raw_rural.xlsx", ag_file = "results_uncertified_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "class_size_elem", disag_file = "results_class_size_elem_disag_raw_rural.xlsx", ag_file = "results_class_size_elem_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "stu_teach_ratio", disag_file = "results_stu_teach_ratio_disag_raw_rural.xlsx", ag_file = "results_stu_teach_ratio_ag_raw.xlsx")

# Urban
# Rural
urban <- df[ which(df$pre_urban == 1),]
run_and_export_main(df = df, outcome = "teacher_uncertified", disag_file = "results_uncertified_disag_raw_urban.xlsx", ag_file = "results_uncertified_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "teacher_out_of_field_fte", disag_file = "results_out_of_field_disag_raw_urban.xlsx", ag_file = "results_uncertified_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "class_size_elem", disag_file = "results_class_size_elem_disag_raw_urban.xlsx", ag_file = "results_class_size_elem_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "stu_teach_ratio", disag_file = "results_stu_teach_ratio_disag_raw_urban.xlsx", ag_file = "results_stu_teach_ratio_ag_raw.xlsx")

# Hispanic
hispanic <- df[ df$pre_hispanic100 == 1,]
run_and_export_main(df = df, outcome = "teacher_uncertified", disag_file = "results_uncertified_disag_raw_hispanic.xlsx", ag_file = "results_uncertified_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "teacher_out_of_field_fte", disag_file = "results_out_of_field_disag_raw_hispanic.xlsx", ag_file = "results_uncertified_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "class_size_elem", disag_file = "results_class_size_elem_disag_raw_hispanic.xlsx", ag_file = "results_class_size_elem_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "stu_teach_ratio", disag_file = "results_stu_teach_ratio_disag_raw_hispanic.xlsx", ag_file = "results_stu_teach_ratio_ag_raw.xlsx")


# Black
black <- df[df$pre_black100 == 1, ]
run_and_export_main(df = df, outcome = "teacher_uncertified", disag_file = "results_uncertified_disag_raw_black.xlsx", ag_file = "results_uncertified_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "teacher_out_of_field_fte", disag_file = "results_out_of_field_disag_raw_black.xlsx", ag_file = "results_uncertified_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "class_size_elem", disag_file = "results_class_size_elem_disag_raw_black.xlsx", ag_file = "results_class_size_elem_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "stu_teach_ratio", disag_file = "results_stu_teach_ratio_disag_raw_black.xlsx", ag_file = "results_stu_teach_ratio_ag_raw.xlsx")

