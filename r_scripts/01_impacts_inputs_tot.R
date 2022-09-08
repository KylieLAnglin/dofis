###
# Main inputs
###
df <- read.csv(paste(data_path, "clean/r_data.csv", sep=""))
df <- df[df$year < 2021, ]
cert <-  read.csv(paste(data_path, "clean/r_data_cert.csv", sep=""))
cert <- cert[cert$year < 2021,]
size <- read.csv(paste(data_path, "clean/r_data_classize.csv", sep=""))
size <- size[size$year < 2021,]

run_and_export_main(df = cert, outcome = "teacher_uncertified", disag_file = "results_uncertified_disag_tot_raw_average.xlsx", ag_file = "results_uncertified_ag_tot_raw_average.xlsx")
run_and_export_main(df = cert, outcome = "teacher_out_of_field_fte", disag_file = "results_out_of_field_disag_tot_raw_average.xlsx", ag_file = "results_out_of_field_ag_tot_raw_average.xlsx")
run_and_export_main(df = size, outcome = "class_size_elem", disag_file = "results_class_size_elem_disag_tot_raw_average.xlsx", ag_file = "results_class_size_elem_ag_tot_raw_average.xlsx")
run_and_export_main(df = size, outcome = "stu_teach_ratio", disag_file = "results_stu_teach_ratio_disag_tot_raw_average.xlsx", ag_file = "results_stu_teach_ratio_ag_tot_raw_average.xlsx")
