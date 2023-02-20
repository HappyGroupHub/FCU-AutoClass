"""This python file will do the AutoClass job."""
import time

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

import utilities as utils

config = utils.read_config()

driver = webdriver.Chrome()


def driver_send_keys(locator, key):
    """Send keys to element.

    :param locator: Locator of element.
    :param key: Keys to send.
    """
    WebDriverWait(driver, 10).until(ec.presence_of_element_located(locator)).send_keys(key)


def driver_click(locator):
    """Click element.

    :param locator: Locator of element.
    """
    WebDriverWait(driver, 10).until(ec.presence_of_element_located(locator)).click()


def driver_screenshot(locator, path):
    """Take screenshot of element.

    :param locator: Locator of element.
    :param path: Path to save screenshot.
    """
    WebDriverWait(driver, 10).until(ec.presence_of_element_located(locator)).screenshot(path)


def driver_get_text(locator):
    """Get text of element.

    :param locator: Locator of element.
    :return: Text of element.
    """
    return WebDriverWait(driver, 10).until(ec.presence_of_element_located(locator)).text


def login():
    """Login to FCU course system."""
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
    """Auto join class script.

    :param class_ids: List of class ids to join.
    """
    driver_click((By.ID, "ctl00_MainContent_TabContainer1_tabSelected_Label3"))
    for class_id in class_ids:
        driver_send_keys((By.ID, "ctl00_MainContent_TabContainer1_tabSelected_tbSubID"), class_id)

        # query remain position
        driver_click((By.XPATH,
                      "//*[@id='ctl00_MainContent_TabContainer1_tabSelected_gvToAdd']/tbody/tr[2]/td[8]/input"))
        time.sleep(0.5)
        alert = driver.switch_to.alert
        remain_pos = alert.text.strip('剩餘名額/開放名額：').split("/")[0]
        alert.accept()

        if not remain_pos == '0':
            driver_click((By.XPATH,
                          "//*[@id='ctl00_MainContent_TabContainer1_tabSelected_gvToAdd']/tbody/tr[2]/td[1]/input"))
            if driver_get_text((By.XPATH,
                                "//*[@id='ctl00_MainContent_TabContainer1_tabSelected_lblMsgBlock']/span")) == "加選成功":
                print("成功加選課程：" + class_id)
                class_ids.remove(class_id)
        else:
            pass
    auto_class(class_ids)


if __name__ == "__main__":
    login()
    driver.quit()
