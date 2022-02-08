

###
# Subgroup Dataframes
###

rural <- df[ which(df$pre_rural == 1),]
urban <- df[ which(df$pre_urban == 1),]

scores25 <- df[ which(df$pre_avescore25==1 | df$pre_avescore50 ==1),]
scores100 <- df[ which(df$pre_avescore75 == 1 | df$pre_avescore100 == 1),]

black25 <- df[ which(df$pre_black25==1 | df$pre_black50 ==1),]
black100 <- df[ which(df$pre_black100 == 1 | df$pre_black75 == 1),]

hisp25 <- df[ which(df$pre_hisp25==1 | df$pre_hisp50 ==1),]
hisp100 <- df[ which(df$pre_hisp100 == 1 | df$pre_hisp75 == 1),]

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

subgroup_desc = c("rural", "urban", "scores25", "scores100", "hisp25", "hisp100", "black25", "black100")
subgroup_dfs = list(rural, urban, scores25, scores100, hisp25, hisp100, black25, black100)

results <- data.frame(subgroup = character(), outcome = character(), te = double(), se = double())

# Math
for (i in 1:length(subgroup_desc)){
  diagg <- attgt_object(subgroup_dfs[i], "math_yr15std")
  agg <- aggte(diagg, type = "simple")
  results[nrow(results) + 1,] = c(subgroup_desc[i], "math_yr15std", agg$overall.att, agg$overall.se)
}

# Reading
for (i in 1:length(subgroup_desc)){
  diagg <- attgt_object(subgroup_dfs[i], "reading_yr15std")
  agg <- aggte(diagg, type = "simple")
  results[nrow(results) + 1,] = c(subgroup_desc[i], "reading_yr15std", agg$overall.att, agg$overall.se)
}

file_name = paste(output_path, "results_subgroup_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)


