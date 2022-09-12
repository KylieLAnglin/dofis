data = df[complete.cases(df[,c("math_yr15std")]),]
rural = data[data$pre_rural == 1, ]
att_gt(yname = "math_yr15std",
       gname = "group",
       idname = "campus",
       tname = "year",
       xformla = ~1 + pre_num + pre_hisp + pre_white + pre_frpl + pre_avescore,
       data = rural,
       control_group = c("notyettreated"), 
       est_method = "reg",
       allow_unbalanced_panel = TRUE,
       clustervars = c("district"),
       print_details = TRUE,
)
