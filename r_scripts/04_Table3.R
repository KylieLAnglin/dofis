home_path = "/Users/kylieanglin/Library/CloudStorage/Dropbox/Active/Research/dofis/"
output_path = paste(home_path, "results/", sep="")
data_path = paste(home_path,"data/", sep = "")
# df <- read.csv(paste(data_path, "clean/r_data.csv", sep=""))

set.seed(42)

library("did")
library("xlsx")

outcomes = c("teacher_uncertified", "teacher_out_of_field_fte", "class_size_elem", "stu_teach_ratio", "teachers_num", "teachers_new_num", "teachers_turnover_ratio_d", "teachers_exp_ave", "days", "days_before_third_week", "minutes_per_day", "minutes", "math_yr15std", "reading_yr15std", "perf_attendance")

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
write.xlsx(x = results, file = paste(output_path, "aggregated_results.xlsx", sep = ""), sheetName = "ag")


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

print_results(df, "teacher_uncertified")
