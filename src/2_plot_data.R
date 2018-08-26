# VISUALIZE TRACKING DATA

library(tidyr)
library(dplyr)
library(RSQLite)
library(lubridate)
library(ggplot2)

# LOAD FROM DATABASE ----
con <- dbConnect(dbDriver("SQLite"), dbname = "data/xiaomi.sqlite")

activity <-
  dbGetQuery(con,
             "SELECT timestamp AS timestamp, steps AS steps,
             heart_rate AS heart_rate
             FROM mi_band_activity_sample")

dbDisconnect(con)

# PREPROCESS ----
# clean data fields
activity_clean <-
  activity %>%
  # timestamp to datetime
  mutate(datetime = as.POSIXct(timestamp, origin = "1970-01-01")) %>% 
  select(-timestamp) %>% 
  # define NA values
  mutate(steps = ifelse(steps <= 0, NA, steps)) %>% 
  mutate(heart_rate = ifelse(heart_rate <= 0 | heart_rate == 255,
                             NA, heart_rate)) %>%
  # filter out rows without data
  filter(!is.na(steps) | !is.na(heart_rate))

# DISTRIBUTIONS ----
# histogram of individual heart rate measurements
ggplot(data = activity_clean, aes(x = heart_rate)) + 
  geom_histogram() +
  theme_bw()

# histogram of steps per day
activity_clean %>% 
  group_by(date = floor_date(datetime, unit = "day")) %>% 
  summarise(steps_sum = sum(steps, na.rm = T)) %>% 
  ungroup %>% 
  ggplot(data = ., aes(x = steps_sum)) + 
  geom_histogram() +
  theme_bw()


# AGGREGATED TIME SERIES ----
# aggregate time intervals
activity_agg <-
  activity_clean %>% 
  group_by(date = floor_date(datetime, unit = "day")) %>% 
  summarise(heart_rate_median = median(heart_rate, na.rm = T),
            steps_sum = sum(steps, na.rm = T)) %>% 
  ungroup

# daily heart rate over time
activity_agg %>%
  gather(measurement, value, -date) %>% 
  ggplot(data = ., aes(x = date, y = value)) +
  geom_line() +
  facet_grid(measurement ~ ., scales = "free_y") +
  theme_bw()
