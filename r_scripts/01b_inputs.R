###
# Main inputs
###
df <- read.csv(paste(data_path, "clean/r_data.csv", sep=""))
df <- df[df$year < 2021, ]

run_and_export_main(df = df, outcome = "teachers_num", disag_file = "results_teachers_num_disag_raw_average.xlsx", ag_file = "results_teachers_num_ag_raw_average.xlsx")
run_and_export_main(df = df, outcome = "teachers_new_num", disag_file = "results_teachers_new_num_disag_raw_average.xlsx", ag_file = "results_teachers_new_num_ag_raw_average.xlsx")
run_and_export_main(df = df, outcome = "teachers_tenure_ave", disag_file = "results_teachers_tenure_ave_disag_raw_average.xlsx", ag_file = "results_teachers_tenure_ave_ag_raw_average.xlsx")
run_and_export_main(df = df, outcome = "teachers_turnover_ratio_d", disag_file = "results_teachers_turnover_ratio_d_disag_raw_average.xlsx", ag_file = "results_teachers_turnover_ratio_d_ag_raw_average.xlsx")

# Rural
rural <- df[ which(df$pre_rural == 1),]
run_and_export_main(df = rural, outcome = "teachers_num", disag_file = "results_teachers_num_disag_raw_rural.xlsx", ag_file = "results_teachers_num_ag_raw_rural.xlsx")
run_and_export_main(df = rural, outcome = "teachers_new_num", disag_file = "results_teachers_new_num_disag_raw_rural.xlsx", ag_file = "results_teachers_new_num_ag_raw_rural.xlsx")
run_and_export_main(df = rural, outcome = "teachers_tenure_ave", disag_file = "results_teachers_tenure_ave_disag_raw_rural.xlsx", ag_file = "results_teachers_tenure_ave_ag_raw_rural.xlsx")
run_and_export_main(df = rural, outcome = "teachers_turnover_ratio_d", disag_file = "results_teachers_turnover_ratio_d_disag_raw_rural.xlsx", ag_file = "results_teachers_turnover_ratio_d_ag_raw_rural.xlsx")

# Urban
urban <- df[ which(df$pre_urban == 1),]
run_and_export_main(df = urban, outcome = "teachers_num", disag_file = "results_teachers_num_disag_raw_urban.xlsx", ag_file = "results_teachers_num_ag_raw_urban.xlsx")
run_and_export_main(df = urban, outcome = "teachers_new_num", disag_file = "results_teachers_new_num_disag_raw_urban.xlsx", ag_file = "results_teachers_new_num_ag_raw_urban.xlsx")
run_and_export_main(df = urban, outcome = "teachers_tenure_ave", disag_file = "results_teachers_tenure_ave_disag_raw_urban.xlsx", ag_file = "results_teachers_tenure_ave_ag_raw_urban.xlsx")
run_and_export_main(df = urban, outcome = "teachers_turnover_ratio_d", disag_file = "results_teachers_turnover_ratio_d_disag_raw_urban.xlsx", ag_file = "results_teachers_turnover_ratio_d_ag_raw_urban.xlsx")

# Hispanic
hispanic <- df[ df$pre_hisp100 == 1,]
run_and_export_main(df = hispanic, outcome = "teachers_num", disag_file = "results_teachers_num_disag_raw_hispanic.xlsx", ag_file = "results_teachers_num_ag_raw_hispanic.xlsx")
run_and_export_main(df = hispanic, outcome = "teachers_new_num", disag_file = "results_teachers_new_num_disag_raw_hispanic.xlsx", ag_file = "results_teachers_new_num_ag_raw_hispanic.xlsx")
run_and_export_main(df = hispanic, outcome = "teachers_tenure_ave", disag_file = "results_teachers_tenure_ave_disag_raw_hispanic.xlsx", ag_file = "results_teachers_tenure_ave_ag_raw_hispanic.xlsx")
run_and_export_main(df = hispanic, outcome = "teachers_turnover_ratio_d", disag_file = "results_teachers_turnover_ratio_d_disag_raw_hispanic.xlsx", ag_file = "results_teachers_turnover_ratio_d_ag_raw_hispanic.xlsx")


# Black
black <- df[df$pre_black100 == 1, ]
run_and_export_main(df = black, outcome = "teachers_num", disag_file = "results_teachers_num_disag_raw_black.xlsx", ag_file = "results_teachers_num_ag_raw_black.xlsx")
run_and_export_main(df = black, outcome = "teachers_new_num", disag_file = "results_teachers_new_num_disag_raw_black.xlsx", ag_file = "results_teachers_new_num_ag_raw_black.xlsx")
run_and_export_main(df = black, outcome = "teachers_tenure_ave", disag_file = "results_teachers_tenure_ave_disag_raw_black.xlsx", ag_file = "results_teachers_tenure_ave_ag_raw_black.xlsx")
run_and_export_main(df = black, outcome = "teachers_turnover_ratio_d", disag_file = "results_teachers_turnover_ratio_d_disag_raw_black.xlsx", ag_file = "results_teachers_turnover_ratio_d_ag_raw_black.xlsx")

# FRPL
frpl <- df[df$pre_frpl100 == 1, ]
run_and_export_main(df = frpl, outcome = "teachers_num", disag_file = "results_teachers_num_disag_raw_frpl.xlsx", ag_file = "results_teachers_num_ag_raw_frpl.xlsx")
run_and_export_main(df = frpl, outcome = "teachers_new_num", disag_file = "results_teachers_new_num_disag_raw_frpl.xlsx", ag_file = "results_teachers_new_num_ag_raw_frpl.xlsx")
run_and_export_main(df = frpl, outcome = "teachers_tenure_ave", disag_file = "results_teachers_tenure_ave_disag_raw_frpl.xlsx", ag_file = "results_teachers_tenure_ave_ag_raw_frpl.xlsx")
run_and_export_main(df = frpl, outcome = "teachers_turnover_ratio_d", disag_file = "results_teachers_turnover_ratio_d_disag_raw_frpl.xlsx", ag_file = "results_teachers_turnover_ratio_d_ag_raw_frpl.xlsx")

# Avescores
avescore <- df[df$pre_avescore100 == 1, ]
run_and_export_main(df = avescore, outcome = "teachers_num", disag_file = "results_teachers_num_disag_raw_avescore.xlsx", ag_file = "results_teachers_num_ag_raw_avescore.xlsx")
run_and_export_main(df = avescore, outcome = "teachers_new_num", disag_file = "results_teachers_new_num_disag_raw_avescore.xlsx", ag_file = "results_teachers_new_num_ag_raw_avescore.xlsx")
run_and_export_main(df = avescore, outcome = "teachers_tenure_ave", disag_file = "results_teachers_tenure_ave_disag_raw_avescore.xlsx", ag_file = "results_teachers_tenure_ave_ag_raw_avescore.xlsx")
run_and_export_main(df = avescore, outcome = "teachers_turnover_ratio_d", disag_file = "results_teachers_turnover_ratio_d_disag_raw_avescore.xlsx", ag_file = "results_teachers_turnover_ratio_d_ag_raw_avescore.xlsx")


