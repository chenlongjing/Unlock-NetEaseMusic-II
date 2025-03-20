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
    browser.add_cookie({"name": "MUSIC_U", "value": "00E8B550AF5012246A382B26FCCE02CAF7DD760424BC8601FA29127AF2906B3F24537970513EB36E16C1BAE90E5B901719E5B012C233FF0C65F0701BA5A692B2905D5E346FD5A1095B24B9A079855ADE71C3DE961292495E9C5F7CB450B9012251A8D59DB3261F7802BCD9960FDB5070E4F94D3004F1359F0B6719AC11410C364060D6D9D525E83AD62EFDE9B5F42878F4EB1F5E7D8AD83D59867E1570703D2244DD088FD892A219C5BEAF5332C2BFBCE9B2FB65086F845A827F8A0B9A5FC71B77A6D30D6FBABE65D447CE4E7141B45E778B71BBCACA43412AC1BC5DE6692E6F5E33D940DA6774E3A15988411CCBBAE8D0FA686F9A8E84D2BF0E7F48909B92BFCE981E13179F81B77E23055C507E472467A1EFF8D240A3F198802A45ADA8A916C98028C4341179F56043C15406AE91D95341C6149CD674A4619A53515310E8F14A0317C0615CD8EF78D653D69D658475DF1D0BECAB66D804251BDDC823627726B0"})
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
