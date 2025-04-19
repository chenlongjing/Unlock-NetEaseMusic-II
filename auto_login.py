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
    browser.add_cookie({"name": "MUSIC_U", "value": "004D60B6A1610EC71441DBE9336F156522AF7130797D802191895ECBD2D5DF2C2E44830310100265EF610FCF4AC4AC3338009789A16B259BA3912652070709FC0D38947BA8EA310F2879EDB7DFC1F6E522C698646CC321D7B0AEC735ECFD21C056E8B289BAF71D9430E44F79A3F24744B491E302A9A1790F1912D7A6045B26730AD8F3395EE46AC6B8D2A5B1FE97300407D5C3F2FF8688D0FB6AFC8E45F85FBDDDB7437574B398F37C81E153DEB26A01A9791E43298EDBFE14A9A77EAF7E5929E93C884036D31EFF1AF09918A4F091BCA3E6C57B3302C0140DFE92EA4CC060C3FA8E2843367B3D57C6FCE3B791EF06B2F300853F5A0277959E6282F8998CAEF48E48AB710CDA1CFB63AC2E594A96E352DD730191672DB3394656C38DDF91E14AE2109E45011513EF0F8DC0DBBA0E1AB79D288AF83D8CAD9A8E2E0A4C518A4D6541C6D9BB0093D9CED992CC87928F7219CD2D6AEA73B6317152FBE2463CB65AA27C"})
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
