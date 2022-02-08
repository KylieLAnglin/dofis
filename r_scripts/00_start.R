home_path = "/Users/kla21002/Dropbox/Active/dofis/"
output_path = paste(home_path, "results/", sep="")
data_path = paste(home_path,"data/", sep = "")
df <- read.csv(paste(data_path, "clean/r_data.csv", sep=""))

set.seed(42)

library("did")
library("openxlsx")