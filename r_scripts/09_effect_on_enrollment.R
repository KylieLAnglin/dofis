attgt.black <- att_gt(yname = "students_black",
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
summary(attgt.black)


attgt.black.results <- data.frame(attgt.black$group, attgt.black$t, attgt.black$att, attgt.black$se)
file_name = paste(output_path, "results_black.xlsx", sep="")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , attgt.black.results, colNames = FALSE)
saveWorkbook(wb,file_name,overwrite = T)

agg.simple.black <- aggte(attgt.black, type = "simple")
agg.dynamic.black <- aggte(attgt.black, type = "dynamic")

agg.results.black <- data.frame(agg.simple.black$overall.att, agg.simple.black$overall.se, agg.dynamic.black$egt, agg.dynamic.black$att.egt, agg.dynamic.black$se.egt)
file_name = paste(output_path, "results_black_ag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , agg.results.black, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

#####

attgt.hisp <- att_gt(yname = "students_hisp",
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
summary(attgt.hisp)

attgt.hisp.results <- data.frame(attgt.hisp$group, attgt.hisp$t, attgt.hisp$att, attgt.hisp$se)
file_name = paste(output_path, "results_hisp.xlsx", sep="")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , attgt.hisp.results, colNames = FALSE)
saveWorkbook(wb,file_name,overwrite = T)

agg.simple.hisp <- aggte(attgt.hisp, type = "simple")
agg.dynamic.hisp <- aggte(attgt.hisp, type = "dynamic")

agg.results.hisp <- data.frame(agg.simple.hisp$overall.att, agg.simple.hisp$overall.se, agg.dynamic.hisp$egt, agg.dynamic.hisp$att.egt, agg.dynamic.hisp$se.egt)
file_name = paste(output_path, "results_hisp_ag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , agg.results.hisp, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

####
attgt.frpl <- att_gt(yname = "students_frpl",
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
summary(attgt.frpl)

attgt.frpl.results <- data.frame(attgt.frpl$group, attgt.frpl$t, attgt.frpl$att, attgt.frpl$se)
file_name = paste(output_path, "results_frpl.xlsx", sep="")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , attgt.hisp.results, colNames = FALSE)
saveWorkbook(wb,file_name,overwrite = T)

agg.simple.frpl <- aggte(attgt.frpl, type = "simple")
agg.dynamic.frpl <- aggte(attgt.frpl, type = "dynamic")

agg.results.frpl <- data.frame(agg.simple.frpl$overall.att, agg.simple.frpl$overall.se, agg.dynamic.frpl$egt, agg.dynamic.frpl$att.egt, agg.dynamic.frpl$se.egt)
file_name = paste(output_path, "results_frpl_ag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , agg.results.frpl, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)
###

attgt.iep <- att_gt(yname = "students_sped",
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
summary(attgt.iep)

attgt.iep.results <- data.frame(attgt.iep$group, attgt.iep$t, attgt.iep$att, attgt.iep$se)
file_name = paste(output_path, "results_iep.xlsx", sep="")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , attgt.iep.results, colNames = FALSE)
saveWorkbook(wb,file_name,overwrite = T)

agg.simple.iep <- aggte(attgt.iep, type = "simple")
agg.dynamic.iep <- aggte(attgt.iep, type = "dynamic")

agg.results.iep <- data.frame(agg.simple.iep$overall.att, agg.simple.iep$overall.se, agg.dynamic.iep$egt, agg.dynamic.iep$att.egt, agg.dynamic.iep$se.egt)
file_name = paste(output_path, "results_iep_ag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , agg.results.iep, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)

## Enrollment

attgt.enrollment <- att_gt(yname = "students_num",
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
summary(attgt.enrollment)

attgt.enrollment.results <- data.frame(attgt.enrollment$group, attgt.enrollment$t, attgt.enrollment$att, attgt.enrollment$se)
file_name = paste(output_path, "results_enrollment.xlsx", sep="")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , attgt.enrollment.results, colNames = FALSE)
saveWorkbook(wb,file_name,overwrite = T)

agg.simple.enrollment <- aggte(attgt.enrollment, type = "simple")
agg.dynamic.enrollment <- aggte(attgt.enrollment, type = "dynamic")

agg.results.enrollment <- data.frame(agg.simple.enrollment$overall.att, agg.simple.enrollment$overall.se, agg.dynamic.enrollment$egt, agg.dynamic.enrollment$att.egt, agg.dynamic.enrollment$se.egt)
file_name = paste(output_path, "results_enrollment_ag_raw.xlsx", sep = "")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , agg.results.enrollment, colNames = TRUE)
saveWorkbook(wb,file_name,overwrite = T)
