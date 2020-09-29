install.packages("furrr")

library(tidyverse)
library(nflfastR)
library(furrr)

setwd('E:/nfl_data/')

pbp_path = 'nflfastR-data/data/play_by_play_2020.csv.gz'

# new game pbp
new_pbp <- fast_scraper('2020_03_KC_BAL')

#Apply cleaning function
cleaned_pbp_qbepa <- add_qb_epa(clean_pbp(new_pbp))

#Optional - Change play types to match if pass or rush == 1
cleaned_pbp_qbepa$play_type[cleaned_pbp_qbepa$pass==1] <- "pass"
cleaned_pbp_qbepa$play_type[cleaned_pbp_qbepa$rush==1] <- "run"

# add expected yards after catch
xyac_pbp <- add_xyac(cleaned_pbp_qbepa)


#Put file path in quotes (C:/Users/Name/Documents/pbp_2020.csv.gz)
#Use file extension .csv.gz for a compressed CSV
write.csv(rbind(read.csv(pbp_path), xyac_pbp), file=gzfile(pbp_path, encoding="UTF-8"), row.names=FALSE)