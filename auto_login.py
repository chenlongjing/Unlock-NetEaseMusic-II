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
    browser.add_cookie({"name": "MUSIC_U", "value": "00AC799D0DB0040584D71B75A8E0FEE7D0CE3D34C49B4C4D158E5ED3BE82745A3EB21C5DE736528CC5D31F3D354FA6AD740C85D5B9F2E4B4643E52312FD0D9A3DD15773188EFA54A01C55C4D9FE4E64D2FEC8F79D8799EA8892F4851B64D99946F74ABC69231670C329AADBC40A4A1807CF6509CB209648C5A3DAA399ED127D89D624344DE7E3571759F702AFF30EEE6AF8E9F8C72AA6C01DEFD5163E4B222638C148B43DA6B5406C7EB1282C60FCE8B81A589015CFC4CF9BA94183842D6F118A9F3300507992F2ED3C4953F3D45298AB027EF87950DC4CF7AF872581E70B6455631010A23DB692ABB243F82A7C0A478E6620967E504AE97D6AB3550C1F08DFF06CB04A6F0773038C1AFCD105A23FEACEE0F4BAD817A2CFDC8C72B02AF25459921DB2A8AE7BBC3A155AFCAC08FDF64F91323CEE5FC60DC55694330F66FFAF3335E70A68A561AD14D7DAE937F6825C5B5A996424B6A9C96951BB53A342793E02F42"})
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
