
###
# Days
###
df <- read.csv(paste(data_path, "clean/r_data.csv", sep=""))

run_and_export_main(df = df, outcome = "days", disag_file = "results_days_disag_raw_average.xlsx", ag_file = "results_days_ag_raw_average.xlsx")
run_and_export_main(df = df, outcome = "days_before_third_week", disag_file = "results_days_before_third_week_disag_raw_average.xlsx", ag_file = "results_days_before_third_week_ag_raw_average.xlsx")
run_and_export_main(df = df, outcome = "minutes_per_day", disag_file = "results_minutes_per_day_disag_raw_average.xlsx", ag_file = "results_minutes_per_day_ag_raw_average.xlsx")
run_and_export_main(df = df, outcome = "minutes", disag_file = "results_minutes_disag_raw_average.xlsx", ag_file = "results_minutes_ag_raw_average.xlsx")

rural <- df[ which(df$pre_rural == 1),]
hispanic <- df[ df$pre_hisp100 == 1,]
black <- df[df$pre_black100 == 1, ]
frpl <- df[df$pre_frpl100 == 1, ]


run_and_export_main(df = rural, outcome = "days", disag_file = "results_days_disag_raw_rural.xlsx", ag_file = "results_days_ag_raw_rural.xlsx")
run_and_export_main(df = hispanic, outcome = "days", disag_file = "results_days_disag_raw_hispanic.xlsx", ag_file = "results_days_ag_raw_hispanic.xlsx")
run_and_export_main(df = black, outcome = "days", disag_file = "results_days_disag_raw_black.xlsx", ag_file = "results_days_ag_raw_black.xlsx")
run_and_export_main(df = frpl, outcome = "days", disag_file = "results_days_disag_raw_frpl.xlsx", ag_file = "results_days_ag_raw_frpl.xlsx")


run_and_export_main(df = rural, outcome = "days_before_third_week", disag_file = "results_days_before_third_week_disag_raw_rural.xlsx", ag_file = "results_days_before_third_week_ag_raw_rural.xlsx")
run_and_export_main(df = hispanic, outcome = "days_before_third_week", disag_file = "results_days_before_third_week_disag_raw_hispanic.xlsx", ag_file = "results_days_before_third_week_ag_raw_hispanic.xlsx")
run_and_export_main(df = black, outcome = "days_before_third_week", disag_file = "results_days_before_third_week_disag_raw_black.xlsx", ag_file = "results_days_before_third_week_ag_raw_black.xlsx")
run_and_export_main(df = frpl, outcome = "days_before_third_week", disag_file = "results_days_before_third_week_disag_raw_frpl.xlsx", ag_file = "results_days_before_third_week_ag_raw_frpl.xlsx")

run_and_export_main(df = rural, outcome = "minutes", disag_file = "results_minutes_disag_raw_rural.xlsx", ag_file = "results_minutes_ag_raw_rural.xlsx")
run_and_export_main(df = hispanic, outcome = "minutes", disag_file = "results_minutes_disag_raw_hispanic.xlsx", ag_file = "results_minutes_ag_raw_hispanic.xlsx")
run_and_export_main(df = black, outcome = "minutes", disag_file = "results_minutes_disag_raw_black.xlsx", ag_file = "results_minutes_ag_raw_black.xlsx")
run_and_export_main(df = frpl, outcome = "minutes", disag_file = "results_minutes_disag_raw_frpl.xlsx", ag_file = "results_minutes_ag_raw_frpl.xlsx")


run_and_export_main(df = rural, outcome = "minutes_per_day", disag_file = "results_minutes_per_day_disag_raw_rural.xlsx", ag_file = "results_minutes_per_day_ag_raw_rural.xlsx")
run_and_export_main(df = hispanic, outcome = "minutes_per_day", disag_file = "results_minutes_per_day_disag_raw_hispanic.xlsx", ag_file = "results_minutes_per_day_ag_raw_hispanic.xlsx")
run_and_export_main(df = black, outcome = "minutes_per_day", disag_file = "results_minutes_per_day_disag_raw_black.xlsx", ag_file = "results_minutes_per_day_ag_raw_black.xlsx")
run_and_export_main(df = frpl, outcome = "minutes_per_day", disag_file = "results_minutes_per_day_disag_raw_frpl.xlsx", ag_file = "results_minutes_per_day_ag_raw_frpl.xlsx")

