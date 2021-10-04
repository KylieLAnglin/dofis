output_path = "/Users/kylieanglin/Dropbox/Active/dofis/results/"
data_path = "/Users/kylieanglin/Dropbox/Active/dofis/data/"
df <- read.csv(paste(data_path, "clean/r_data_school_2020_comparison.csv", sep=""))

set.seed(42)

library(did)
library("openxlsx")