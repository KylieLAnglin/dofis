attgt.black <- att_gt(yname = "students_black",
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
summary(attgt.black)


attgt.black.results <- data.frame(attgt.black$group, attgt.black$t, attgt.black$att, attgt.black$se)
file_name = paste(output_path, "results_black.xlsx", sep="")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , attgt.black.results, colNames = FALSE)
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
                      allow_unbalanced_panel = TRUE,
                      clustervars = c("district"),
                      print_details = TRUE
)
summary(attgt.hisp)

attgt.hisp.results <- data.frame(attgt.hisp$group, attgt.hisp$t, attgt.hisp$att, attgt.hisp$se)
file_name = paste(output_path, "results_hisp.xlsx", sep="")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , attgt.hisp.results, colNames = FALSE)
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
                     allow_unbalanced_panel = TRUE,
                     clustervars = c("district"),
                     print_details = TRUE
)
summary(attgt.frpl)

attgt.frpl.results <- data.frame(attgt.frpl$group, attgt.frpl$t, attgt.frpl$att, attgt.frpl$se)
file_name = paste(output_path, "results_frpl.xlsx", sep="")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , attgt.hisp.results, colNames = FALSE)
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
                     allow_unbalanced_panel = TRUE,
                     clustervars = c("district"),
                     print_details = TRUE
)
summary(attgt.iep)

attgt.iep.results <- data.frame(attgt.iep$group, attgt.iep$t, attgt.iep$att, attgt.iep$se)
file_name = paste(output_path, "results_iep.xlsx", sep="")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , attgt.iep.results, colNames = FALSE)
saveWorkbook(wb,file_name,overwrite = T)


attgt.enrollment <- att_gt(yname = "students_num",
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
summary(attgt.enrollment)

attgt.enrollment.results <- data.frame(attgt.enrollment$group, attgt.enrollment$t, attgt.enrollment$att, attgt.enrollment$se)
file_name = paste(output_path, "results_enrollment.xlsx", sep="")
wb <- loadWorkbook(file_name)
writeData(wb, sheet = "raw" , attgt.enrollment.results, colNames = FALSE)
saveWorkbook(wb,file_name,overwrite = T)


