library(did)
library("openxlsx")


disag.math <- att_gt(yname = "math_yr15std",
                     gname = "group",
                     idname = "campus",
                     tname = "year",
                     xformla = ~1,
                     data = df,
                     control_group = c("notyettreated"), 
                     est_method = "reg",
                     allow_unbalanced_panel = FALSE,
                     clustervars = c("district"),
                     print_details = TRUE,
                     bstrap = TRUE
)
disag.math.results <- data.frame(disag.math$group, disag.math$t, disag.math$att, disag.math$se, disag.math$n)
file_name = paste(output_path, "results_math_disag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , disag.math.results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

ggdid(disag.math)

agg.simple.math <- aggte(disag.math, type = "simple")
summary(agg.simple.math)

agg.dynamic.math <- aggte(disag.math, type = "dynamic")
summary(agg.dynamic.math)
ggdid(agg.dynamic.math)




agg.results.math <- data.frame(agg.simple.math$overall.att, agg.simple.math$overall.se, agg.dynamic.math$egt, agg.dynamic.math$att.egt, agg.dynamic.math$se.egt)
file_name = paste(output_path, "results_math_ag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , agg.results.math, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

###
# Reading
###

disag.reading <- att_gt(yname = "reading_yr15std",
                     gname = "group",
                     idname = "campus",
                     tname = "year",
                     xformla = ~1,
                     data = df,
                     control_group = c("notyettreated"), 
                     est_method = "reg",
                     allow_unbalanced_panel = FALSE,
                     clustervars = c("district"),
                     print_details = TRUE,
)

disag.reading.results <- data.frame(disag.reading$group, disag.reading$t, disag.reading$att, disag.reading$se, disag.reading$n)
file_name = paste(output_path, "results_reading_disag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , disag.reading.results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

agg.simple.reading <- aggte(disag.reading, type = "simple")
summary(agg.simple.reading)

agg.dynamic.reading <- aggte(disag.reading, type = "dynamic")
summary(agg.dynamic.reading)

agg.results.reading <- data.frame(agg.simple.reading$overall.att, agg.simple.reading$overall.se, agg.dynamic.reading$egt, agg.dynamic.reading$att.egt, agg.dynamic.reading$se.egt)
file_name = paste(output_path, "results_reading_ag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , agg.results.reading, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)


## Uncertified Teachers
disag.cert <- att_gt(yname = "teachers_uncertified",
                gname = "group",
                idname = "campus",
                tname = "year",
                xformla = ~1,
                data = df,
                control_group = c("notyettreated"), 
                est_method = "reg",
                allow_unbalanced_panel = FALSE,
                clustervars = c("district"),
                print_details = TRUE,
)
disag.cert.results <- data.frame(disag.cert$group, disag.cert$t, disag.cert$att, disag.cert$se, disag.cert$n)
file_name = paste(output_path, "results_uncertified_disag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , disag.cert.results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

ggdid(disag.cert)
agg.cert.simple <- aggte(disag.cert, type = "simple")
summary(agg.cert.simple)

agg.cert.dynamic <- aggte(disag.cert, type = "dynamic")
summary(agg.cert.dynamic)
ggdid(agg.cert.dynamic)


agg.cert.results <- data.frame(agg.cert.simple$overall.att, agg.cert.simple$overall.se, agg.cert.dynamic$egt, agg.cert.dynamic$att.egt, agg.cert.dynamic$se.egt)
file_name = paste(output_path, "results_uncertified_ag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , agg.cert.results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)


# Class Sizes
disag.classsize <- att_gt(yname = "class_size_elem",
                gname = "group",
                idname = "campus",
                tname = "year",
                xformla = ~1,
                data = df,
                control_group = c("notyettreated"), 
                est_method = "reg",
                allow_unbalanced_panel = FALSE,
                clustervars = c("district"),
                print_details = TRUE,
)
disag.classsize.results <- data.frame(disag.classsize$group, disag.classsize$t, disag.classsize$att, disag.classsize$se, disag.classsize$n)
file_name = paste(output_path, "results_class_size_elem_disag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , disag.classsize.results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

ggdid(disag.classsize)

agg.classsize.simple <- aggte(disag.classsize, type = "simple")
summary(agg.classsize.simple)

agg.classsize.dynamic <- aggte(disag.classsize, type = "dynamic")
summary(agg.classsize.dynamic)
ggdid(agg.classsize.dynamic)


agg.classsize.results <- data.frame(agg.classsize.simple$overall.att, agg.classsize.simple$overall.se, agg.classsize.dynamic$egt, agg.classsize.dynamic$att.egt, agg.classsize.dynamic$se.egt)
file_name = paste(output_path, "results_class_size_elem_ag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , agg.classsize.results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)




## Out of field math
disag.cert.math <- att_gt(yname = "teachers_secondary_math_outoffield",
                gname = "group",
                idname = "campus",
                tname = "year",
                xformla = ~1,
                data = df,
                control_group = c("notyettreated"), 
                est_method = "reg",
                allow_unbalanced_panel = FALSE,
                clustervars = c("district"),
                print_details = TRUE,
)
disag.cert.math.results <- data.frame(disag.cert.math$group, disag.cert.math$t, disag.cert.math$att, disag.cert.math$se, disag.cert.math$n)
file_name = paste(output_path, "results_outoffield_math_disag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , disag.cert.math.results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

ggdid(disag.cert.math)

agg.cert.math.simple <- aggte(disag.cert.math, type = "simple")
summary(agg.cert.math.simple)

agg.cert.math.dynamic <- aggte(disag.cert.math, type = "dynamic")
summary(agg.cert.math.dynamic)
ggdid(agg.cert.math.dynamic)


agg.cert.math.results <- data.frame(agg.cert.math.simple$overall.att, agg.cert.math.simple$overall.se, agg.cert.math.dynamic$egt, agg.cert.math.dynamic$att.egt, agg.cert.math.dynamic$se.egt)
file_name = paste(output_path, "results_outoffield_math_ag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , agg.cert.math.results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

## Out of field secondary
disag.cert.science <- att_gt(yname = "teachers_secondary_science_outoffield",
                gname = "group",
                idname = "campus",
                tname = "year",
                xformla = ~1,
                data = df,
                control_group = c("notyettreated"), 
                est_method = "reg",
                allow_unbalanced_panel = FALSE,
                clustervars = c("district"),
                print_details = TRUE,
)
disag.cert.science.results <- data.frame(disag.cert.science$group, disag.cert.science$t, disag.cert.science$att, disag.cert.science$se, disag.cert.science$n)
file_name = paste(output_path, "results_outoffield_science_disag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , disag.cert.science.results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

ggdid(disag.cert.science)

agg.cert.science.simple <- aggte(disag.cert.science, type = "simple")
summary(agg.cert.science.simple)

agg.cert.science.dynamic <- aggte(disag.cert.science, type = "dynamic")
summary(agg.cert.science.dynamic)
ggdid(agg.cert.science.dynamic)

agg.cert.science.results <- data.frame(agg.cert.science.simple$overall.att, agg.cert.science.simple$overall.se, agg.cert.science.dynamic$egt, agg.cert.science.dynamic$att.egt, agg.cert.science.dynamic$se.egt)
file_name = paste(output_path, "results_outoffield_science_ag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , agg.cert.science.results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)


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

results <- data.frame(outcome = character(), te = double(), se = double())

for (i in 1:length(outcomes)){
  diagg <- attgt_object(df, outcomes[i])
  agg <- aggte(diagg, type = "simple")
  results[nrow(results) + 1,] = c(outcomes[i], agg$overall.att, agg$overall.se)
}

file_name = paste(output_path, "results_overall_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

