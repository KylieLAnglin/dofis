df <- read.csv(paste(data_path, "clean/r_data.csv", sep=""))


run_and_export_main(df = df, outcome = "teacher_uncertified_extreme", disag_file = "results_uncertified_disag_raw_extreme.xlsx", ag_file = "results_uncertified_ag_raw_extreme.xlsx")
run_and_export_main(df = df, outcome = "teacher_out_of_field_extreme", disag_file = "results_out_of_field_disag_raw_extreme.xlsx", ag_file = "results_out_of_field_ag_raw_extreme.xlsx")
run_and_export_main(df = df, outcome = "class_size_elem_extreme", disag_file = "results_class_size_elem_disag_raw_extreme.xlsx", ag_file = "results_class_size_elem_ag_raw_extreme.xlsx")
run_and_export_main(df = df, outcome = "stu_teach_ratio_extreme", disag_file = "results_stu_teach_ratio_disag_raw_extreme.xlsx", ag_file = "results_stu_teach_ratio_ag_raw_extreme.xlsx")


home_path = "/Users/kylieanglin/Library/CloudStorage/Dropbox/Active/Research/dofis/"
output_path = paste(home_path, "results/", sep="")
data_path = paste(home_path,"data/", sep = "")
# df <- read.csv(paste(data_path, "clean/r_data.csv", sep=""))

set.seed(42)

library("did")
library("xlsx")

outcomes = c("teacher_uncertified_extreme", "teacher_out_of_field_extreme", "class_size_elem_extreme", "stu_teach_ratio_extreme")

return_att <- function(df, outcome){
  disag <- att_gt(yname = outcome,
                  gname = "group",
                  idname = "campus",
                  tname = "year",
                  xformla = ~1 + pre_num + pre_hisp + pre_white + pre_frpl + pre_avescore,
                  data = df,
                  control_group = c("notyettreated"), 
                  est_method = "reg",
                  allow_unbalanced_panel = FALSE,
                  clustervars = c("district"),
                  print_details = TRUE,
  )
  
  agg.simple <- aggte(disag, type = "simple")
  
  return(agg.simple$overall.att)
  #  summary(agg.simple)  
  
}

return_se <- function(df, outcome){
  disag <- att_gt(yname = outcome,
                  gname = "group",
                  idname = "campus",
                  tname = "year",
                  xformla = ~1 + pre_num + pre_hisp + pre_white + pre_frpl + pre_avescore,
                  data = df,
                  control_group = c("notyettreated"), 
                  est_method = "reg",
                  allow_unbalanced_panel = FALSE,
                  clustervars = c("district"),
                  print_details = TRUE,
  )
  
  agg.simple <- aggte(disag, type = "simple")
  
  return(agg.simple$overall.se)
  
}

tes <- list() #create an empty list
ses <- list()

for (i in 1:length(outcomes)) {
  tes = append(tes, return_att(df = df, outcome = outcomes[i]))
  ses = append(ses, return_se(df = df, outcome = outcomes[i]))
  
}


# tes = append(tes, return_att(df = df, outcome = "teacher_uncertified"))
# ses = append(ses, return_se(df = df, outcome = "teacher_uncertified"))
lists = list(outcomes = outcomes, tes = tes, ses = ses)
results = as.data.frame(do.call(cbind, lists))
write.xlsx(x = results, file = paste(output_path, "aggregated_results_extremes.xlsx", sep = ""), sheetName = "ag")


print_results <- function(df, outcome){
  disag <- att_gt(yname = outcome,
                  gname = "group",
                  idname = "campus",
                  tname = "year",
                  xformla = ~1 + pre_num + pre_hisp + pre_white + pre_frpl + pre_avescore,
                  data = df,
                  control_group = c("notyettreated"), 
                  est_method = "reg",
                  allow_unbalanced_panel = FALSE,
                  clustervars = c("district"),
                  print_details = TRUE,
  )
  
  agg.simple <- aggte(disag, type = "simple")
  return(agg.simple)
}

print_results(df, "teacher_uncertified_extreme")
