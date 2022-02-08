## Overall
library(did)
library("openxlsx")
df_ever <- read.csv(paste(data_path, "clean/r_data_ever.csv", sep=""))

inputs = c("teachers_uncertified", "teachers_secondary_math_outoffield", "teachers_secondary_science_outoffield", "teachers_secondary_cte_outoffield")

exempt_certification <- df[df$exempt_certification == 1, ]
exempt_classsize <- df[df$exempt_classsize == 1, ]


attgt_object <- function(df, y) {
  att.gt <- att_gt(yname = y,
                   gname = "group",
                   idname = "campus",
                   tname = "year",
                   xformla = ~1,
                   data = df_ever,
                   control_group = c("notyettreated"), 
                   est_method = "reg",
                   allow_unbalanced_panel = FALSE,
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

diagg <- attgt_object(exempt_classsize, "class_size_elem")
agg <- aggte(diagg, type = "simple")
results[nrow(results) + 1,] = c("exempt_classsize", "class_size_mean_elem", agg$overall.att, agg$overall.se)

file_name = paste(output_path, "results_ever_inputs_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

## Uncertified Teachers
disag <- att_gt(yname = "teachers_uncertified",
                     gname = "group",
                     idname = "campus",
                     tname = "year",
                     xformla = ~1,
                     data = df_ever,
                     control_group = c("notyettreated"), 
                     est_method = "reg",
                     allow_unbalanced_panel = FALSE,
                     clustervars = c("district"),
                     print_details = TRUE,
)
disag.results <- data.frame(disag$group, disag$t, disag$att, disag$se, disag$n)
file_name = paste(output_path, "results_ever_uncertified_disag_raw.xlsx", sep = "")
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
file_name = paste(output_path, "results_ever_uncertified_ag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , agg.results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

## Out of field math
disag <- att_gt(yname = "teachers_secondary_math_outoffield",
                gname = "group",
                idname = "campus",
                tname = "year",
                xformla = ~1,
                data = df_ever,
                control_group = c("notyettreated"), 
                est_method = "reg",
                allow_unbalanced_panel = FALSE,
                clustervars = c("district"),
                print_details = TRUE,
)
disag.results <- data.frame(disag$group, disag$t, disag$att, disag$se, disag$n)
file_name = paste(output_path, "results_ever_outoffield_math_disag_raw.xlsx", sep = "")
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
file_name = paste(output_path, "results_ever_outoffield_math_ag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , agg.results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

## Out of field secondary
disag <- att_gt(yname = "teachers_secondary_science_outoffield",
                gname = "group",
                idname = "campus",
                tname = "year",
                xformla = ~1,
                data = df_ever,
                control_group = c("notyettreated"), 
                est_method = "reg",
                allow_unbalanced_panel = FALSE,
                clustervars = c("district"),
                print_details = TRUE,
)
disag.results <- data.frame(disag$group, disag$t, disag$att, disag$se, disag$n)
file_name = paste(output_path, "results_ever_outoffield_science_disag_raw.xlsx", sep = "")
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
file_name = paste(output_path, "results_ever_outoffield_science_ag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , agg.results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

### Out of field CTE
disag <- att_gt(yname = "teachers_secondary_cte_outoffield",
                gname = "group",
                idname = "campus",
                tname = "year",
                xformla = ~1,
                data = df_ever,
                control_group = c("notyettreated"), 
                est_method = "reg",
                allow_unbalanced_panel = FALSE,
                clustervars = c("district"),
                print_details = TRUE,
)
disag.results <- data.frame(disag$group, disag$t, disag$att, disag$se, disag$n)
file_name = paste(output_path, "results_ever_outoffield_cte_disag_raw.xlsx", sep = "")
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
file_name = paste(output_path, "results_ever_outoffield_cte_ag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , agg.results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

# Class Sizes
disag <- att_gt(yname = "class_size_elem",
                gname = "group",
                idname = "campus",
                tname = "year",
                xformla = ~1,
                data = df_ever,
                control_group = c("notyettreated"), 
                est_method = "reg",
                allow_unbalanced_panel = FALSE,
                clustervars = c("district"),
                print_details = TRUE,
)
disag.results <- data.frame(disag$group, disag$t, disag$att, disag$se, disag$n)
file_name = paste(output_path, "results_ever_class_size_elem_disag_raw.xlsx", sep = "")
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
file_name = paste(output_path, "results_ever_class_size_elem_ag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , agg.results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

