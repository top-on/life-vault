# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 18:28:08 2017

@author: Thorben Jensen
"""
#%% IMPORTS

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import getpass
from selenium.webdriver.common.by import By
import glob
import shutil
from os.path import expanduser
import time


#%% OPEN LOGIN

driver = webdriver.Chrome()
driver.get("https://myaccount.google.com/intro")

assert "My Account" in driver.title

elem = driver.find_element_by_id("gb_70")
elem.send_keys(Keys.RETURN)

assert "Sign in" in driver.title


#%% DO LOGIN

username = input('Username: ')
elem = driver.find_element_by_name("Email")
elem.clear()
elem.send_keys(username)
elem.send_keys(Keys.RETURN)

password = getpass.getpass('Password:')
elem = driver.find_element_by_name("Passwd")
elem.clear()
elem.send_keys(password)
elem.send_keys(Keys.RETURN)


#%% ACCESS 'TAKEOUT LIGHT'

driver.get('https://takeout.google.com/settings/takeout/light')

# uncheck all boxes
elems = driver.find_elements(By.XPATH, "//input[@class='gr']");
for elem in elems:
    elem.click()
    
# check 'fit' box
elems = driver.find_elements(By.XPATH, 
  "//input[contains(@class, 'gr') and contains(@value, 'fit')]")
elems[0].click()

elems = driver.find_elements(By.XPATH, 
  "//input[contains(@class, 'Moa gr')]")
elems[0].click()


#%% DOWNLOAD LATEST ARCHIVE

print('Waiting 20s for archive to be prepared...')
time.sleep(20)

print('Downloading archive...')
driver.get('https://takeout.google.com/settings/takeout/light')
elem = driver.find_element(By.XPATH, "//a[contains(., 'Download')]")
elem.click()

if 'Sign in' in driver.title:
    print('Re-entering your password...')
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)

    print('Downloading file...') 
    driver.get('https://takeout.google.com/settings/takeout/light')
    elem = driver.find_element(By.XPATH, "//a[contains(., 'Download')]")
    elem.click()
    
print('Waiting 5s for download to finish...')
time.sleep(5)


#%% MOVE DOWNLOADED FILE TO ~/backup/fit/.

home = expanduser("~")
source_dir = home + '/Downloads/'
dest_dir = home + "/backup/takeout/raw"

for file in glob.glob(r''+ source_dir +'takeout-*.zip'):
    print('Moving takeout file '+ file +' to backup folder: '+ dest_dir)                                                                                                                                        
    shutil.move(file, dest_dir)


#%% LOGOUT AND CLOSE DRIVER

print('Done. Logging out.')
driver.find_element(By.XPATH, '//span[@class="gb_9a gbii"]').click()
driver.find_element(By.XPATH, '//a[@id="gb_71"]').click()
driver.close()
