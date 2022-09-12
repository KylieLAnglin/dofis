df <- read.csv(paste(data_path, "clean/r_data.csv", sep=""))

run_and_export_main(df = df, outcome = "math_yr15std", disag_file = "results_math_yr15std_average_disag_raw.xlsx", ag_file = "results_math_yr15std_average_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "math_black_yr15std", disag_file = "results_math_yr15std_black_disag_raw.xlsx", ag_file = "results_math_yr15std_black_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "math_hisp_yr15std", disag_file = "results_math_yr15std_hispanic_disag_raw.xlsx", ag_file = "results_math_yr15std_hispanic_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "math_white_yr15std", disag_file = "results_math_yr15std_white_disag_raw.xlsx", ag_file = "results_math_yr15std_white_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "math_frpl_yr15std", disag_file = "results_math_yr15std_frpl_disag_raw.xlsx", ag_file = "results_math_yr15std_frpl_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "math_sped_yr15std", disag_file = "results_math_yr15std_sped_disag_raw.xlsx", ag_file = "results_math_yr15std_sped_ag_raw.xlsx")

run_and_export_main(df = df, outcome = "reading_yr15std", disag_file = "results_reading_yr15std_average_disag_raw.xlsx", ag_file = "results_reading_yr15std_average_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "reading_black_yr15std", disag_file = "results_reading_yr15std_black_disag_raw.xlsx", ag_file = "results_reading_yr15std_black_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "reading_hisp_yr15std", disag_file = "results_reading_yr15std_hispanic_disag_raw.xlsx", ag_file = "results_reading_yr15std_hispanic_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "reading_white_yr15std", disag_file = "results_yr15std_white_disag_raw.xlsx", ag_file = "results_reading_yr15std_white_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "reading_frpl_yr15std", disag_file = "results_yr15std_frpl_disag_raw.xlsx", ag_file = "results_reading_yr15std_frpl_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "reading_sped_yr15std", disag_file = "results_yr15std_sped_disag_raw.xlsx", ag_file = "results_reading_yr15std_sped_ag_raw.xlsx")

run_and_export_main(df = df, outcome = "perf_attendance", disag_file = "results_perf_attendance_average_disag_raw.xlsx", ag_file = "results_perf_attendance_average_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "perf_attendance_black", disag_file = "results_perf_attendance_black_disag_raw.xlsx", ag_file = "results_perf_attendance_black_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "perf_attendance_hispanic", disag_file = "results_perf_attendanc_hispanic_disag_raw.xlsx", ag_file = "results_perf_attendance_hispanic_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "perf_attendance_frpl", disag_file = "results_perf_attendance_frpl_disag_raw.xlsx", ag_file = "results_perf_attendance_frpl_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "perf_attendance_sped", disag_file = "results_perf_attendance_sped_disag_raw.xlsx", ag_file = "results_perf_attendance_sped_ag_raw.xlsx")



rural <- df[df$pre_rural == 1, ]
rural <- rural[complete.cases(rural[,c("math_yr15std")]),]
run_and_export_main(df = rural, outcome = "math_yr15std", disag_file = "results_math_yr15std_rural_disag_raw.xlsx", ag_file = "results_math_yr15std_rural_ag_raw.xlsx")
run_and_export_main(df = rural, outcome = "reading_yr15std", disag_file = "results_reading_yr15std_rural_disag_raw.xlsx", ag_file = "results_reading_yr15std_rural_ag_raw.xlsx")
run_and_export_main(df = rural, outcome = "perf_attendance", disag_file = "results_perf_attendance_rural_disag_raw.xlsx", ag_file = "results_perf_attendance_rural_ag_raw.xlsx")

