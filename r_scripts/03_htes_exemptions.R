library(did)
library("openxlsx")
output_path = "/Users/kylie/dofis/results/"



attgt_object <- function(df, y) {
  att.gt <- att_gt(yname = y,
                   gname = "group",
                   idname = "campus",
                   tname = "year",
                   xformla = ~1,
                   data = df,
                   control_group = c("notyettreated"), 
                   est_method = "reg",
                   allow_unbalanced_panel = TRUE,
                   clustervars = c("district"),
                   print_details = TRUE
  )
  
  
  return(att.gt)
}

df <- read.csv("~/dofis/data/clean/r_data_school_2020_comparison.csv")

results_by_exemptions <- data.frame(subgroup = character(), exempt = integer(), outcome = character(), te = double(), se = double())

exemptions <- c("exempt_firstday", 
                   "exempt_minutes", 
                   "exempt_lastday", 
                   "exempt_certification", 
                   "exempt_probation", 
                   "exempt_servicedays", 
                   "exempt_eval", 
                   "exempt_classsize", 
                   "exempt_attendance", 
                   "exempt_behavior")


for (i in 1:length(exemptions)){
  exempt_df <- df[df[, exemptions[i]] == 1, ]
  diagg <- attgt_object(exempt_df, "math_yr15std")
  agg <- aggte(diagg, type = "simple")
  results_by_exemptions[nrow(results_by_exemptions) + 1,] = c(exemptions[i], 1, "math_yr15std", agg$overall.att, agg$overall.se)
  
  not_exempt_df <- df[df[, exemptions[i]] == 0, ]
  diagg <- attgt_object(not_exempt_df, "math_yr15std")
  agg <- aggte(diagg, type = "simple")
  results_by_exemptions[nrow(results_by_exemptions) + 1,] = c(exemptions[i], 0, "math_yr15std", agg$overall.att, agg$overall.se)
}

for (i in 1:length(exemptions)){
  exempt_df <- df[df[, exemptions[i]] == 1, ]
  diagg <- attgt_object(exempt_df, "reading_yr15std")
  agg <- aggte(diagg, type = "simple")
  results_by_exemptions[nrow(results_by_exemptions) + 1,] = c(exemptions[i], 1, "reading_yr15std", agg$overall.att, agg$overall.se)
  
  not_exempt_df <- df[df[, exemptions[i]] == 0, ]
  diagg <- attgt_object(not_exempt_df, "reading_yr15std")
  agg <- aggte(diagg, type = "simple")
  results_by_exemptions[nrow(results_by_exemptions) + 1,] = c(exemptions[i], 0, "reading_yr15std", agg$overall.att, agg$overall.se)
}

file_name = paste(output_path, "results_exemptions_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , results_by_exemptions, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)


exempt_df <- df[df["exempt_servicedays"] == 1, ]
diagg <- attgt_object(exempt_df, "math_yr15std")
agg <- aggte(diagg, type = "simple")

exempt_servicedays <- data.frame(diagg$group, diagg$t, diagg$att, diagg$se, diagg$n)
file_name = paste(output_path, "exempt_servicedays_disag_math.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , exempt_servicedays, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

####

exempt_df <- df[df["exempt_servicedays"] == 1, ]
diagg <- attgt_object(exempt_df, "reading_yr15std")
agg <- aggte(diagg, type = "simple")

exempt_servicedays <- data.frame(diagg$group, diagg$t, diagg$att, diagg$se, diagg$n)
file_name = paste(output_path, "exempt_servicedays_disag_reading.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , exempt_servicedays, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)