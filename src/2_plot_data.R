# VISUALIZE TRACKING DATA

library(dplyr)
library(RSQLite)
library(lubridate)
library(ggplot2)

# LOAD FROM DATABASE ----
con <- dbConnect(dbDriver("SQLite"), dbname = "data/xiaomi.sqlite")

activity <-
  dbGetQuery(con,
             "SELECT timestamp, steps, heart_rate
             FROM mi_band_activity_sample")

dbDisconnect(con)

# PREPROCESS ----
act_clean <-
  activity %>%
  # timestamp to datetime and date 
  mutate(datetime = as.POSIXct(TIMESTAMP, origin="1970-01-01")) %>% 
  mutate(date = as_date(datetime)) %>% 
  select(-TIMESTAMP) %>% 
  # define NA values
  mutate(STEPS = ifelse(STEPS == 0, NA, STEPS)) %>% 
  mutate(HEART_RATE = ifelse(HEART_RATE == 0 | HEART_RATE == 255,
                             NA, HEART_RATE)) %>%
  # filter out rows without data
  filter(!is.na(STEPS) | !is.na(HEART_RATE))

# VISUALIZE ----

# daily heart rate over time
act_clean %>% 
  group_by(date) %>% 
  summarise(median_hr = median(HEART_RATE, na.rm = T)) %>% 
  ungroup %>% 
  ggplot(data = ., aes(x = date, y = median_hr)) +
  geom_line() +
  theme_bw()

# step activity over time
# TODO
