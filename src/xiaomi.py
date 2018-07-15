# LOADING AND ANALYZING WRISTBAND DATA

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import sqlite3
import pandas as pd

# authenticate
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# download database
file_list = \
    drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
xiaomi_file = [i for i in file_list if i['title'] == 'xiaomi.sqlite'][0]
xiaomi_file.GetContentFile('data/xiaomi.sqlite')

# database to CSV
con = sqlite3.connect('data/xiaomi.sqlite')
sql = '''SELECT timestamp, heart_rate
         FROM mi_band_activity_sample'''
df = pd.read_sql(sql, con)
con.close()

# clean data
df = df[(df.HEART_RATE < 255) & (df.HEART_RATE > 0)]
df.describe()

# plot histogram
# TODO

# plot time series
# TODO
