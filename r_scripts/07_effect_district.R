district_df <- read.csv(paste(data_path, "clean/r_data_district_2020_comparison.csv", sep=""))

set.seed(42)


disag.math <- att_gt(yname = "math_yr15std",
                     gname = "group",
                     idname = "district",
                     tname = "year",
                     xformla = ~1,
                     data = district_df,
                     control_group = c("notyettreated"), 
                     est_method = "reg",
                     allow_unbalanced_panel = TRUE,
                     clustervars = c("district"),
                     print_details = TRUE,
)

disag.math.results <- data.frame(disag.math$group, disag.math$t, disag.math$att, disag.math$se, disag.math$n)
file_name = paste(output_path, "results_math_disag_raw_district.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , disag.math.results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

agg.simple.math <- aggte(disag.math, type = "simple")
summary(agg.simple.math)

agg.dynamic.math <- aggte(disag.math, type = "dynamic")
summary(agg.dynamic.math)




agg.results.math <- data.frame(agg.simple.math$overall.att, agg.simple.math$overall.se, agg.dynamic.math$egt, agg.dynamic.math$att.egt, agg.dynamic.math$se.egt)
file_name = paste(output_path, "results_math_ag_raw_district.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , agg.results.math, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

###
# Reading
###

disag.reading <- att_gt(yname = "reading_yr15std",
                        gname = "group",
                        idname = "district",
                        tname = "year",
                        xformla = ~1,
                        data = district_df,
                        control_group = c("notyettreated"), 
                        est_method = "reg",
                        allow_unbalanced_panel = TRUE,
                        clustervars = c("district"),
                        print_details = TRUE,
)

disag.reading.results <- data.frame(disag.reading$group, disag.reading$t, disag.reading$att, disag.reading$se, disag.reading$n)
file_name = paste(output_path, "results_reading_disag_raw_district.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , disag.reading.results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

agg.simple.reading <- aggte(disag.reading, type = "simple")
summary(agg.simple.reading)

agg.dynamic.reading <- aggte(disag.reading, type = "dynamic")
summary(agg.dynamic.reading)

agg.results.reading <- data.frame(agg.simple.reading$overall.att, agg.simple.reading$overall.se, agg.dynamic.reading$egt, agg.dynamic.reading$att.egt, agg.dynamic.reading$se.egt)
file_name = paste(output_path, "results_reading_ag_raw_district.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , agg.results.reading, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)