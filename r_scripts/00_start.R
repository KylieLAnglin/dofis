home_path = "/Users/kla21002/Dropbox/Active/dofis/"
output_path = paste(home_path, "results/", sep="")
data_path = paste(home_path,"data/", sep = "")
df <- read.csv(paste(data_path, "clean/r_data.csv", sep=""))

set.seed(42)

library("did")
library("openxlsx")

run_and_export_main <- function(df, outcome, disag_file, ag_file){
  disag <- att_gt(yname = outcome,
                       gname = "group",
                       idname = "campus",
                       tname = "year",
                       xformla = ~1 + pre_num + pre_hisp + + pre_frpl + pre_sped + pre_ell + pre_white + pre_black + pre_tenure + pre_turnover,
                       data = df,
                       control_group = c("notyettreated"), 
                       est_method = "reg",
                       allow_unbalanced_panel = FALSE,
                       clustervars = c("district"),
                       print_details = TRUE,
  )
  disag.results <- data.frame(disag$group, disag$t, disag$att, disag$se, disag$n)
  file_name = paste(output_path, disag_file, sep = "")
  wb <- loadWorkbook(file_name)
  writeData(wb, sheet = "raw" , disag.results, colNames = TRUE)
  saveWorkbook(wb,file_name,overwrite = T)
  
  ggdid(disag)
  agg.simple <- aggte(disag, type = "simple")
  summary(agg.simple)  
  
  agg.dynamic <- aggte(disag, type = "dynamic")
  summary(agg.dynamic)
  ggdid(agg.dynamic)
  
  agg.results <- data.frame(agg.simple$overall.att, agg.simple$overall.se, agg.dynamic$egt, agg.dynamic$att.egt, agg.dynamic$se.egt)
  file_name = paste(output_path, ag_file, sep = "")
  wb <- loadWorkbook(file_name)
  writeData(wb, sheet = "raw" , agg.results, colNames = TRUE)
  saveWorkbook(wb,file_name,overwrite = T)
}










