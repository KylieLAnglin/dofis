df <- read.csv("~/dofis/data/clean/r_data_school_2020_comparison.csv")

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


outcomes = c("m_3rd_yr15std", "m_4th_yr15std", "m_5th_yr15std", "m_6th_yr15std", "m_7th_yr15std", "m_8th_yr15std", "alg_yr15std", 
                  "r_3rd_yr15std", "r_4th_yr15std", "r_5th_yr15std", "r_6th_yr15std", "r_7th_yr15std", "r_8th_yr15std", "eng1_yr15std")

results <- data.frame(outcome = character(), te = double(), se = double())

for (i in 1:length(outcomes)){
  diagg <- attgt_object(exempt_certification, outcomes[i])
  agg <- aggte(diagg, type = "simple")
  results[nrow(results) + 1,] = c(outcomes[i], agg$overall.att, agg$overall.se)
}

file_name = "/Users/kylie/dofis/results/Who Needs Rules/results_subjects_raw.xlsx"
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

