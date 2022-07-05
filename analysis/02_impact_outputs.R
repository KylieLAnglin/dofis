# 
df <- read.csv(paste(data_path, "clean/r_data.csv", sep=""))
run_and_export_main(df = df, outcome = "math_yr15std", disag_file = "results_temp_disag_raw.xlsx", ag_file = "results_temp_ag_raw.xlsx")
