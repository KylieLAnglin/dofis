home_path = "/Users/kylieanglin/Library/CloudStorage/Dropbox/Active/Research/dofis/"
output_path = paste(home_path, "results/", sep="")
data_path = paste(home_path,"data/", sep = "")
df <- read.csv(paste(data_path, "clean/r_data.csv", sep=""))

set.seed(42)

library("did")
library("xlsx")
run_and_export_main <- function(df, outcome, disag_file, ag_file){
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
  disag.results <- data.frame(disag$group, disag$t, disag$att, disag$se, disag$n)
  file_name = paste(output_path, disag_file, sep = "")
  
  wb = createWorkbook()
  write.xlsx(x = disag.results, file = file_name, sheetName = "disag")
  
  ggdid(disag)
  agg.simple <- aggte(disag, type = "simple")
  summary(agg.simple)  
  
  agg.dynamic <- aggte(disag, type = "dynamic")
  summary(agg.dynamic)
  ggdid(agg.dynamic)
  
  agg.results <- data.frame(agg.simple$overall.att, agg.simple$overall.se, agg.dynamic$egt, agg.dynamic$att.egt, agg.dynamic$se.egt)
  file_name = paste(output_path, ag_file, sep = "")
  wb = createWorkbook()
  write.xlsx(x = agg.results, file = file_name, sheetName = "ag")
  

}



run_and_export_nomatch <- function(df, outcome, disag_file, ag_file){
  disag <- att_gt(yname = outcome,
                  gname = "group",
                  idname = "campus",
                  tname = "year",
                  xformla = ~1 ,
                  data = df,
                  control_group = c("notyettreated"), 
                  est_method = "reg",
                  allow_unbalanced_panel = FALSE,
                  clustervars = c("district"),
                  print_details = TRUE,
  )
  disag.results <- data.frame(disag$group, disag$t, disag$att, disag$se, disag$n)
  file_name = paste(output_path, disag_file, sep = "")
  
  wb = createWorkbook()
  write.xlsx(x = disag.results, file = file_name, sheetName = "disag")
  
  ggdid(disag)
  agg.simple <- aggte(disag, type = "simple")
  summary(agg.simple)  
  
  agg.dynamic <- aggte(disag, type = "dynamic")
  summary(agg.dynamic)
  ggdid(agg.dynamic)
  
  agg.results <- data.frame(agg.simple$overall.att, agg.simple$overall.se, agg.dynamic$egt, agg.dynamic$att.egt, agg.dynamic$se.egt)
  file_name = paste(output_path, ag_file, sep = "")
  wb = createWorkbook()
  write.xlsx(x = agg.results, file = file_name, sheetName = "ag")

}

run_and_export_weights <- function(df, outcome, disag_file, ag_file){
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
                  weightsname = "students_num"
  )
  disag.results <- data.frame(disag$group, disag$t, disag$att, disag$se, disag$n)
  file_name = paste(output_path, disag_file, sep = "")
  
  wb = createWorkbook()
  write.xlsx(x = disag.results, file = file_name, sheetName = "disag")
  
  ggdid(disag)
  agg.simple <- aggte(disag, type = "simple")
  summary(agg.simple)  
  
  agg.dynamic <- aggte(disag, type = "dynamic")
  summary(agg.dynamic)
  ggdid(agg.dynamic)
  
  agg.results <- data.frame(agg.simple$overall.att, agg.simple$overall.se, agg.dynamic$egt, agg.dynamic$att.egt, agg.dynamic$se.egt)
  file_name = paste(output_path, ag_file, sep = "")
  wb = createWorkbook()
  write.xlsx(x = agg.results, file = file_name, sheetName = "ag")
  
}


