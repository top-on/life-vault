# DOWNLOAD DATABASE FROM GOOGLE DRIVE

library(googledrive)

# drive_auth()

drive_find(q = "'root' in parents") %>% 
  filter(name == "xiaomi.sqlite") %>% 
  drive_download(path = "data/xiaomi.sqlite", overwrite = TRUE)
