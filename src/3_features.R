# FEATURE ENGINEERING AND SELECTION

library(dplyr)

# LOAD DATA ----
load("data/processed/activity_agg.Rdata")

# function for lagging features
lags <- function(var, indices = 1:10) {
  var <- enquo(var)
  purrr::map( indices, ~quo(lag(!!var, !!.x)) ) %>% 
    purrr::set_names(sprintf("%s_lag_%02d", rlang::quo_text(var), indices))
}

# engineer features ----
activity_features <-
  activity_agg %>% 
  # lagged_features
  mutate(!!!lags(steps_sum),
         !!!lags(hr_0.25))

# TEST FEATURES WITH LM ----
lm(activity_features, formula = hr_0.25 ~ .) %>% 
  summary
