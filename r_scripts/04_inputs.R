library(did)
library("openxlsx")
output_path = "/Users/kylie/dofis/results/"

df <- read.csv("~/dofis/data/clean/r_data_school_2020_comparison.csv")


inputs = c("teachers_uncertified", "teachers_secondary_math_outoffield", "teachers_secondary_science_outoffield", "teachers_secondary_cte_outoffield")

exempt_certification <- df[df$exempt_certification == 1, ]
exempt_classsize <- df[df$exempt_classsize == 1, ]

# "class_size_mean_elem"

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

results <- data.frame(subgroup = character(), outcome = character(), te = double(), se = double())

for (i in 1:length(inputs)){
  diagg <- attgt_object(exempt_certification, inputs[i])
  agg <- aggte(diagg, type = "simple")
  results[nrow(results) + 1,] = c("exempt_certification", inputs[i], agg$overall.att, agg$overall.se)
}

diagg <- attgt_object(exempt_classsize, "class_size_mean_elem")
agg <- aggte(diagg, type = "simple")
results[nrow(results) + 1,] = c("exempt_classsize", "class_size_mean_elem", agg$overall.att, agg$overall.se)

file_name = paste(output_path, "results_inputs_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)


