###
# Main inputs
###
df <- read.csv(paste(data_path, "clean/r_data.csv", sep=""))

# Uncertified teachers
# df <- read.csv(paste(data_path, "clean/r_data_cert.csv", sep=""))
run_and_export_main(df = df, outcome = "teacher_uncertified", disag_file = "results_uncertified_disag_raw.xlsx", ag_file = "results_uncertified_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "teacher_out_of_field_fte", disag_file = "results_out_of_field_disag_raw.xlsx", ag_file = "results_uncertified_ag_raw.xlsx")

# Elementary class sizes
# df <- read.csv(paste(data_path, "clean/r_data_classsize.csv", sep=""))
run_and_export_main(df = df, outcome = "class_size_elem", disag_file = "results_class_size_elem_disag_raw.xlsx", ag_file = "results_class_size_elem_ag_raw.xlsx")

# Student-teacher ratio
# df <- read.csv(paste(data_path, "clean/r_data.csv", sep=""))
run_and_export_main(df = df, outcome = "stu_teach_ratio", disag_file = "results_stu_teach_ratio_disag_raw.xlsx", ag_file = "results_stu_teach_ratio_ag_raw.xlsx")

# Teacher salary
run_and_export_main(df = df, outcome = "teacher_salary_ave", disag_file = "results_stu_teach_ratio_disag_raw.xlsx", ag_file = "results_stu_teach_ratio_ag_raw.xlsx")

run_and_export_main(df = df, outcome = "teachers_exp_ave", disag_file = "results_temp_disag_raw.xlsx", ag_file = "results_temp_ag_raw.xlsx")
run_and_export_main(df = df, outcome = "teachers_tenure_ave", disag_file = "results_temp_disag_raw.xlsx", ag_file = "results_temp_ag_raw.xlsx")


###
# Main inputs - subgroups
###
# Uncertified teachers
df <- read.csv(paste(data_path, "clean/r_data_cert.csv", sep=""))
df <- df[df$pre_black100 == 1,]
run_and_export_main(df = df, outcome = "teachers_uncertified", disag_file = "results_uncertified_disag_raw_black.xlsx", ag_file = "results_uncertified_ag_raw_black.xlsx")

df <- read.csv(paste(data_path, "clean/r_data_cert.csv", sep=""))
df <- df[df$pre_hisp100 == 1,]
run_and_export_main(df = df, outcome = "teachers_uncertified", disag_file = "results_uncertified_disag_raw_hisp.xlsx", ag_file = "results_uncertified_ag_raw_hisp.xlsx")

df <- read.csv(paste(data_path, "clean/r_data_cert.csv", sep=""))
df <- df[df$pre_rural == 1,]
run_and_export_main(df = df, outcome = "teachers_uncertified", disag_file = "results_uncertified_disag_raw_rural.xlsx", ag_file = "results_uncertified_ag_raw_rural.xlsx")

df <- read.csv(paste(data_path, "clean/r_data_cert.csv", sep=""))
df <- df[df$pre_frpl100 == 1,]
run_and_export_main(df = df, outcome = "teachers_uncertified", disag_file = "results_uncertified_disag_raw_frpl.xlsx", ag_file = "results_uncertified_ag_raw_frpl.xlsx")


###
# Appendices
###

# Out of field math
df <- read.csv(paste(data_path, "clean/r_data_cert.csv", sep=""))
run_and_export_main(df = df, outcome = "teachers_secondary_math_outoffield", disag_file = "results_outoffield_math_disag_raw.xlsx", ag_file = "results_outoffield_math_ag_raw.xlsx")

# Out of field science
df <- read.csv(paste(data_path, "clean/r_data_cert.csv", sep=""))
run_and_export_main(df = df, outcome = "teachers_secondary_science_outoffield", disag_file = "results_outoffield_science_disag_raw.xlsx", ag_file = "results_outoffield_science_ag_raw.xlsx")


## Overall
outcomes = c("math_yr15std", "reading_yr15std", "teachers_uncertified", "class_size_elem", "teachers_secondary_math_outoffield", "teachers_secondary_science_outoffield")

attgt_object <- function(df, y) {
  att.gt <- att_gt(yname = y,
                   gname = "group",
                   idname = "campus",
                   tname = "year",
                   xformla = ~1,
                   data = df,
                   control_group = c("notyettreated"), 
                   est_method = "reg",
                   allow_unbalanced_panel = FALSE,
                   clustervars = c("district"),
                   print_details = TRUE
  )
  
  
  return(att.gt)
}

results <- data.frame(outcome = character(), te = double(), se = double(), n = double())

for (i in 1:length(outcomes)){
  diagg <- attgt_object(df, outcomes[i])
  agg <- aggte(diagg, type = "simple")
  results[nrow(results) + 1,] = c(outcomes[i], agg$overall.att, agg$overall.se, agg$DIDparams$n)
}

file_name = paste(output_path, "results_overall_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

