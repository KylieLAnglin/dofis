###
# Main inputs
###
df <- read.csv(paste(data_path, "clean/r_data.csv", sep=""))


run_and_export_weights(df = df, outcome = "teacher_uncertified", disag_file = "results_uncertified_disag_raw_average_weights.xlsx", ag_file = "results_uncertified_ag_raw_average_weights.xlsx")
run_and_export_weights(df = df, outcome = "teacher_out_of_field_fte", disag_file = "results_out_of_field_disag_raw_average_weights.xlsx", ag_file = "results_out_of_field_ag_raw_average_weights.xlsx")
run_and_export_weights(df = df, outcome = "class_size_elem", disag_file = "results_class_size_elem_disag_raw_average_weights.xlsx", ag_file = "results_class_size_elem_ag_raw_average_weights.xlsx")
run_and_export_weights(df = df, outcome = "stu_teach_ratio", disag_file = "results_stu_teach_ratio_disag_raw_average_weights.xlsx", ag_file = "results_stu_teach_ratio_ag_raw_average_weights.xlsx")

# Rural
rural <- df[ which(df$pre_rural == 1),]
run_and_export_weights(df = rural, outcome = "teacher_uncertified", disag_file = "results_uncertified_disag_raw_rural_weights.xlsx", ag_file = "results_uncertified_ag_raw_rural_weights.xlsx")
run_and_export_weights(df = rural, outcome = "teacher_out_of_field_fte", disag_file = "results_out_of_field_disag_raw_rural_weights.xlsx", ag_file = "results_out_of_field_ag_raw_rural_weights.xlsx")
run_and_export_weights(df = rural, outcome = "class_size_elem", disag_file = "results_class_size_elem_disag_raw_rural_weights.xlsx", ag_file = "results_class_size_elem_ag_raw_rural_weights.xlsx")
run_and_export_weights(df = rural, outcome = "stu_teach_ratio", disag_file = "results_stu_teach_ratio_disag_raw_rural_weights.xlsx", ag_file = "results_stu_teach_ratio_ag_raw_rural_weights.xlsx")

# Urban
urban <- df[ which(df$pre_urban == 1),]
run_and_export_weights(df = urban, outcome = "teacher_uncertified", disag_file = "results_uncertified_disag_raw_urban_weights.xlsx", ag_file = "results_uncertified_ag_raw_urban_weights.xlsx")
run_and_export_weights(df = urban, outcome = "teacher_out_of_field_fte", disag_file = "results_out_of_field_disag_raw_urban_weights.xlsx", ag_file = "results_out_of_field_ag_raw_urban_weights.xlsx")
run_and_export_weights(df = urban, outcome = "class_size_elem", disag_file = "results_class_size_elem_disag_raw_urban_weights.xlsx", ag_file = "results_class_size_elem_ag_raw_urban_weights.xlsx")
run_and_export_weights(df = urban, outcome = "stu_teach_ratio", disag_file = "results_stu_teach_ratio_disag_raw_urban_weights.xlsx", ag_file = "results_stu_teach_ratio_ag_raw_urban_weights.xlsx")

# Hispanic
hispanic <- df[ df$pre_hisp100 == 1,]
run_and_export_weights(df = hispanic, outcome = "teacher_uncertified", disag_file = "results_uncertified_disag_raw_hispanic_weights.xlsx", ag_file = "results_uncertified_ag_raw_hispanic_weights.xlsx")
run_and_export_weights(df = hispanic, outcome = "teacher_out_of_field_fte", disag_file = "results_out_of_field_disag_raw_hispanic_weights.xlsx", ag_file = "results_out_of_field_ag_raw_hispanic_weights.xlsx")
run_and_export_weights(df = hispanic, outcome = "class_size_elem", disag_file = "results_class_size_elem_disag_raw_hispanic_weights.xlsx", ag_file = "results_class_size_elem_ag_raw_hispanic_weights.xlsx")
run_and_export_weights(df = hispanic, outcome = "stu_teach_ratio", disag_file = "results_stu_teach_ratio_disag_raw_hispanic_weights.xlsx", ag_file = "results_stu_teach_ratio_ag_raw_hispanic_weights.xlsx")


# Black
black <- df[df$pre_black100 == 1, ]
run_and_export_weights(df = black, outcome = "teacher_uncertified", disag_file = "results_uncertified_disag_raw_black_weights.xlsx", ag_file = "results_uncertified_ag_raw_black_weights.xlsx")
run_and_export_weights(df = black, outcome = "teacher_out_of_field_fte", disag_file = "results_out_of_field_disag_raw_black_weights.xlsx", ag_file = "results_out_of_field_ag_raw_black_weights.xlsx")
run_and_export_weights(df = black, outcome = "class_size_elem", disag_file = "results_class_size_elem_disag_raw_black_weights.xlsx", ag_file = "results_class_size_elem_ag_raw_black_weights.xlsx")
run_and_export_weights(df = black, outcome = "stu_teach_ratio", disag_file = "results_stu_teach_ratio_disag_raw_black_weights.xlsx", ag_file = "results_stu_teach_ratio_ag_raw_black_weights.xlsx")

# FRPL
frpl <- df[df$pre_frpl100 == 1, ]
run_and_export_weights(df = frpl, outcome = "teacher_uncertified", disag_file = "results_uncertified_disag_raw_frpl_weights.xlsx", ag_file = "results_uncertified_ag_raw_frpl_weights.xlsx")
run_and_export_weights(df = frpl, outcome = "teacher_out_of_field_fte", disag_file = "results_out_of_field_disag_raw_frpl_weights.xlsx", ag_file = "results_out_of_field_ag_raw_frpl_weights.xlsx")
run_and_export_weights(df = frpl, outcome = "class_size_elem", disag_file = "results_class_size_elem_disag_raw_frpl_weights.xlsx", ag_file = "results_class_size_elem_ag_raw_frpl_weights.xlsx")
run_and_export_weights(df = frpl, outcome = "stu_teach_ratio", disag_file = "results_stu_teach_ratio_disag_raw_frpl_weights.xlsx", ag_file = "results_stu_teach_ratio_ag_raw_frpl_weights.xlsx")

# Avescores
avescore <- df[df$pre_avescore100 == 1, ]
run_and_export_weights(df = avescore, outcome = "teacher_uncertified", disag_file = "results_uncertified_disag_raw_avescore_weights.xlsx", ag_file = "results_uncertified_ag_raw_avescore_weights.xlsx")
run_and_export_weights(df = avescore, outcome = "teacher_out_of_field_fte", disag_file = "results_out_of_field_disag_raw_avescore_weights.xlsx", ag_file = "results_out_of_field_ag_raw_avescore_weights.xlsx")
run_and_export_weights(df = avescore, outcome = "class_size_elem", disag_file = "results_class_size_elem_disag_raw_avescore_weights.xlsx", ag_file = "results_class_size_elem_ag_raw_avescore_weights.xlsx")
run_and_export_weights(df = avescore, outcome = "stu_teach_ratio", disag_file = "results_stu_teach_ratio_disag_raw_avescore_weights.xlsx", ag_file = "results_stu_teach_ratio_ag_raw_avescore_weights.xlsx")


