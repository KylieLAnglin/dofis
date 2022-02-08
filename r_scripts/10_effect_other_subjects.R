library(did)
library("openxlsx")

# Biology
disag.bio <- att_gt(yname = "biology_yr15std",
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

disag.bio.results <- data.frame(disag.bio$group, disag.bio$t, disag.bio$att, disag.bio$se, disag.bio$n)
file_name = paste(output_path, "results_bio_disag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , disag.bio.results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

ggdid(disag.bio)

agg.simple.bio <- aggte(disag.bio, type = "simple")
summary(agg.simple.bio)

agg.dynamic.bio <- aggte(disag.bio, type = "dynamic")
summary(agg.dynamic.bio)
ggdid(agg.dynamic.bio)




agg.results.bio <- data.frame(agg.simple.bio$overall.att, agg.simple.bio$overall.se, agg.dynamic.bio$egt, agg.dynamic.bio$att.egt, agg.dynamic.bio$se.egt)
file_name = paste(output_path, "results_bio_ag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , agg.results.bio, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)


# US History
disag.us <- att_gt(yname = "us_yr15std",
                     gname = "group",
                     idname = "campus",
                     tname = "year",
                     xformla = ~1 + pre_num + pre_hisp + + pre_frpl + pre_sped + pre_ell + pre_white + pre_black + pre_tenure + pre_turnover,
                     data = df[df$year > 2013,],
                     control_group = c("notyettreated"), 
                     est_method = "reg",
                     allow_unbalanced_panel = FALSE,
                     clustervars = c("district"),
                     print_details = TRUE,
)
disag.us.results <- data.frame(disag.us$group, disag.us$t, disag.us$att, disag.us$se, disag.us$n)
file_name = paste(output_path, "results_us_disag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , disag.us.results, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

ggdid(disag.us)

agg.simple.us <- aggte(disag.us, type = "simple")
summary(agg.simple.us)

agg.dynamic.us <- aggte(disag.us, type = "dynamic")
summary(agg.dynamic.us)
ggdid(agg.dynamic.us)


agg.results.us <- data.frame(agg.simple.us$overall.att, agg.simple.us$overall.se, agg.dynamic.us$egt, agg.dynamic.us$att.egt, agg.dynamic.us$se.egt)
file_name = paste(output_path, "results_us_ag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , agg.results.us, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)