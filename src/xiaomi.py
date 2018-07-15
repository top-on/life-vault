# LOADING AND ANALYZING WRISTBAND DATA

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import sqlite3
import pandas as pd
from matplotlib import pyplot as plt


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
plt.figure()
hist = df.HEART_RATE.hist(bins=40, xrot=45)
fig = hist.get_figure()
fig.savefig('results/histogram.png')

# heatrates per date (median and lower quartile)
df2 = df
df2['TIMESTAMP'] = pd.to_datetime(df2['TIMESTAMP'], unit='s')
df2['date'] = df2.TIMESTAMP.dt.date
df_median = df2.groupby('date')['HEART_RATE'].median()
df_lower_quartile = df2.groupby('date')['HEART_RATE'].quantile(q=0.25)

# plot median over time
plt.figure()
line = df_median.plot.line()
fig = line.get_figure()
fig.savefig('results/timeseries_median.png', )

# plot lower quartile over time
plt.figure()
line = df_median.plot.line()
fig = line.get_figure()
locs, labels = plt.xticks()
plt.setp(labels, rotation=45)
fig.savefig('results/timeseries_lower_quartile.png', bbox_inches='tight')
