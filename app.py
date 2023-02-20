"""This python file will do the AutoClass job."""

from selenium import webdriver
from selenium.common import TimeoutException
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


def driver_screenshot(locator, path):
    WebDriverWait(driver, 10).until(ec.presence_of_element_located(locator)).screenshot(path)


def login():
    driver.get('https://course.fcu.edu.tw/')
    driver_send_keys((By.ID, "ctl00_Login1_UserName"), config.get("username"))
    driver_send_keys((By.ID, "ctl00_Login1_Password"), config.get("password"))
    driver_screenshot((By.ID, "ctl00_Login1_Image1"), "captcha.png")
    driver_send_keys((By.ID, "ctl00_Login1_vcode"), utils.get_ocr_answer("captcha.png"))
    driver_click((By.ID, "ctl00_Login1_LoginButton"))
    try:
        WebDriverWait(driver, 1).until(ec.presence_of_element_located((By.ID, "ctl00_btnLogout")))
    except TimeoutException:
        print("Login Failed, relog now.")
        login()
    auto_class(config.get("class_ids"))


def auto_class(class_ids):
    driver_click((By.ID, "ctl00_MainContent_TabContainer1_tabSelected_Label3"))
    for class_id in class_ids:
        driver_send_keys((By.ID, "ctl00_MainContent_TabContainer1_tabSelected_tbSubID"), class_id)
        try:
            WebDriverWait(driver, 0.5).until(ec.presence_of_element_located((By.ID,
                                                                             "//*[@id='ctl00_MainContent_TabContainer1_tabSelected_gvToDel']/tbody/tr[2]/td[1]/input")))
            class_ids.remove(class_id)
        except TimeoutException:
            driver_click((By.XPATH,
                          "//*[@id='ctl00_MainContent_TabContainer1_tabSelected_gvToAdd']/tbody/tr[2]/td[1]/input"))
    auto_class(class_ids)


if __name__ == "__main__":
    login()
    driver.quit()
