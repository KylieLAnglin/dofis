df <- read.csv(paste(data_path, "clean/r_data.csv", sep=""))
run_and_export_main(df = df, outcome = "students_black", disag_file = "results_black_disag_raw.xlsx", ag_file = "results_black_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "students_hisp", disag_file = "results_hisp_disag_raw.xlsx", ag_file = "results_hisp_ag_raw.xlsx")
run_and_export_nomatch(df = df, outcome = "students_frpl", disag_file = "results_frpl_disag_raw.xlsx", ag_file = "results_frpl_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "students_num", disag_file = "results_students_num_disag_raw.xlsx", ag_file = "results_students_num_ag_raw.xlsx")

