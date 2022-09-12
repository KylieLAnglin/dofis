df <- read.csv(paste(data_path, "clean/r_data.csv", sep=""))
df <- df[df$year < 2020, ]

run_and_export_main(df = df, outcome = "math_yr15std", disag_file = "results_math_yr15std_disag_raw.xlsx", ag_file = "results_math_yr15std_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "math_black_yr15std", disag_file = "results_math_black_yr15std_disag_raw.xlsx", ag_file = "results_math_black_yr15std_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "math_hisp_yr15std", disag_file = "results_math_hisp_yr15std_disag_raw.xlsx", ag_file = "results_hisp_yr15std_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "math_white_yr15std", disag_file = "results_white_yr15std_disag_raw.xlsx", ag_file = "results_white_yr15std_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "math_frpl_yr15std", disag_file = "results_frpl_yr15std_disag_raw.xlsx", ag_file = "results_frpl_yr15std_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "math_sped_yr15std", disag_file = "results_sped_yr15std_disag_raw.xlsx", ag_file = "results_sped_yr15std_ag_raw.xlsx")

run_and_export_main(df = df, outcome = "reading_yr15std", disag_file = "results_reading_yr15std_disag_raw.xlsx", ag_file = "results_reading_yr15std_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "reading_black_yr15std", disag_file = "results_reading_black_yr15std_disag_raw.xlsx", ag_file = "results_reading_black_yr15std_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "reading_hisp_yr15std", disag_file = "results_reading_hisp_yr15std_disag_raw.xlsx", ag_file = "results_hisp_yr15std_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "reading_white_yr15std", disag_file = "results_white_yr15std_disag_raw.xlsx", ag_file = "results_white_yr15std_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "reading_frpl_yr15std", disag_file = "results_frpl_yr15std_disag_raw.xlsx", ag_file = "results_frpl_yr15std_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "reading_sped_yr15std", disag_file = "results_sped_yr15std_disag_raw.xlsx", ag_file = "results_sped_yr15std_ag_raw.xlsx")

rural <- df[df$pre_rural == 1, ]
rural <- rural[complete.cases(rural[,c("math_yr15std")]),]
run_and_export_main(df = rural, outcome = "math_yr15std", disag_file = "results_math_rural_yr15std_disag_raw.xlsx", ag_file = "results_math_rural_yr15std_ag_raw.xlsx")
run_and_export_main(df = rural, outcome = "reading_yr15std", disag_file = "results_reading_rural_yr15std_disag_raw.xlsx", ag_file = "results_reading_rural_yr15std_ag_raw.xlsx")

