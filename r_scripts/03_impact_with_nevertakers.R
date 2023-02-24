###
# Main inputs
###
df <- read.csv(paste(data_path, "clean/r_data_w_nevertakers.csv", sep=""))



run_and_export_main(df = df, outcome = "teacher_uncertified", disag_file = "results_w_nevertakers_uncertified_disag_raw_average.xlsx", ag_file = "results_w_nevertakers_uncertified_ag_raw_average.xlsx")
run_and_export_main(df = df, outcome = "teacher_out_of_field_fte", disag_file = "results_w_nevertakers_out_of_field_disag_raw_average.xlsx", ag_file = "results_w_nevertakers_out_of_field_ag_raw_average.xlsx")
run_and_export_main(df = df, outcome = "class_size_elem", disag_file = "results_w_nevertakers_class_size_elem_disag_raw_average.xlsx", ag_file = "results_w_nevertakers_class_size_elem_ag_raw_average.xlsx")
run_and_export_main(df = df, outcome = "stu_teach_ratio", disag_file = "results_w_nevertakers_stu_teach_ratio_disag_raw_average.xlsx", ag_file = "results_w_nevertakers_stu_teach_ratio_ag_raw_average.xlsx")

df2 <- df[df$year < 2021, ]


run_and_export_main(df = df2, outcome = "math_yr15std", disag_file = "results_w_nevertakers_math_yr15std_average_disag_raw.xlsx", ag_file = "results_w_nevertakers_math_yr15std_average_ag_raw.xlsx")
run_and_export_main(df = df2, outcome = "reading_yr15std", disag_file = "results_w_nevertakers_reading_yr15std_average_disag_raw.xlsx", ag_file = "results_w_nevertakers_reading_yr15std_average_ag_raw.xlsx")
run_and_export_main(df = df2, outcome = "perf_attendance", disag_file = "results_w_nevertakers_perf_attendance_average_disag_raw.xlsx", ag_file = "results_w_nevertakers_perf_attendance_average_ag_raw.xlsx")
