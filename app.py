"""This python file will do the AutoClass job."""
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

import utilities as utils

config = utils.read_config()

driver = webdriver.Chrome()


def driver_send_keys(locator, key):
    WebDriverWait(driver, 10).until(ec.presence_of_element_located(locator)).send_keys(key)


def driver_click(locator):
    WebDriverWait(driver, 10).until(ec.presence_of_element_located(locator)).click()


def login():
    driver.get('https://course.fcu.edu.tw/')
    driver_send_keys((By.ID, "ctl00_Login1_UserName"), config.get("username"))
    driver_send_keys((By.ID, "ctl00_Login1_Password"), config.get("password"))


login()
time.sleep(100)
