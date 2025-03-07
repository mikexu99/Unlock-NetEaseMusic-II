# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00728A9C784E3586A192E9EBE4D5A7766436D3FE71CA95DD5B3DED62537B4E489B3C51DD202BE9362DC0E98D34899C2F677CB9F86509197BC8D52A2D36553270859A4D627FE338D9CCB144B673C6A842E9936EF0D3925FEA08C918515FEAD88F389F072137DC80950B74BEA267DB0F1B9B9350E24B7A7AD606DF18B19C7FE72B3EFF69A4315D2F6E0E5B9A49FF953FFC7BDC37E23AB3BD30508B24B3472ECE491F0F73CBD72BE906FA856FF51D48398254AD6219EF56F7E86B821B1214FAF576BD488D1B6529F955E3C7C109EC5930610F85D31B633D4196237EBED3CC14C483755DA17BA44726C174D33E8B0E5077F81C8189B1B6517465829555F2F09F6ED2AFFC023A72BE76DED0DE87892BB2F83858F319FDFE4CC36BB4953F36B8BA214AF24011B0C7401977753021F56BF8335B2034554DF43AAA3A7B5B49EF4FD7FECA3CC93C8DB6C224F65BECCEF4D8ACE99704C997D2CA6694F5C034D1CEC0ECFE2FD2"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
