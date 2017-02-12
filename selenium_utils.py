# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 12:14:25 2017

@author: thor
"""

import getpass
from selenium.webdriver.common.by import By
    
def send_user_input(element, prompt):
    username = getpass.getpass(prompt)
    element.clear()
    element.send_keys(username)

def click_xpath(driver, path):
    driver.find_element(By.XPATH, path).click()
    
def click_all_xpaths(driver, path):
    elements = driver.find_elements(By.XPATH, path)
    for element in elements:
        element.click()