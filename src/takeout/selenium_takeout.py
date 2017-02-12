# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 18:28:08 2017

@author: Thorben Jensen
"""
#%% IMPORTS

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import glob
import shutil
from os.path import expanduser
import time
from selenium_utils import send_user_input
from selenium_utils import click_xpath
from selenium_utils import click_all_xpaths

#%% OPEN LOGIN

driver = webdriver.Chrome()
driver.get("https://myaccount.google.com/intro")

assert "My Account" in driver.title

elem = driver.find_element_by_id("gb_70")
elem.send_keys(Keys.RETURN)

assert "Sign in" in driver.title


#%% DO LOGIN

elem = driver.find_element_by_name("Email")
send_user_input(element=elem, prompt='Username: ')
elem.send_keys(Keys.RETURN)

# waiting
while True:
    if len(driver.find_elements_by_name("Passwd")) > 0: 
        break
    time.sleep(1)

elem = driver.find_element_by_name("Passwd")
send_user_input(element=elem, prompt='Password: ')
elem.send_keys(Keys.RETURN)


#%% ACCESS 'TAKEOUT LIGHT'

assert "My Account" in driver.title

driver.get('https://takeout.google.com/settings/takeout/light')

# uncheck all boxes
click_all_xpaths(driver, "//input[@class='gr']")
    
# check 'fit' box
click_xpath(driver, 
            "//input[contains(@class, 'gr') and contains(@value, 'fit')]")

click_xpath(driver, "//input[contains(@class, 'Moa gr')]")


#%% DOWNLOAD LATEST ARCHIVE

print('Waiting 20s for archive to be prepared...')
time.sleep(20)

print('Downloading archive...')
driver.get('https://takeout.google.com/settings/takeout/light')
click_xpath(driver, "//a[contains(., 'Download')]")

if 'Sign in' in driver.title:
    print('Re-entering your password...')
    elem = driver.find_element_by_name("Passwd")
    send_user_input(element=elem, prompt='Password: ')
    elem.send_keys(Keys.RETURN)

    print('Downloading file...') 
    driver.get('https://takeout.google.com/settings/takeout/light')
    click_xpath(driver, "//a[contains(., 'Download')]")    
    
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
click_xpath(driver, '//span[@class="gb_9a gbii"]')
click_xpath(driver, '//a[@id="gb_71"]')
driver.close()
