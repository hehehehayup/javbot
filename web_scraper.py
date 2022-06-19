'''
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os
import time


def init_browser():
    options = Options()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    #options.add_argument("--headless")
    #options.add_argument("--disable-dev-shm-usage")
    #options.add_argument("--no-sandbox")
    # service = Service(os.environ.get("CHROMEDRIVER_PATH"))
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

code = "SSIS-004"
browser = init_browser()
browser.get("https://www.javlibrary.com/en/")
time.sleep(3)
if browser.find_element(By.ID, 'adultwarningprompt'):
    warning = browser.find_element(By.XPATH,"//input[@type='button' and @value='I agree.']")
    warning.click()
search_box = browser.find_element(By.ID,'idsearchbox')
search_box.send_keys(code)
search_box = browser.find_element(By.ID, 'idsearchbutton')
search_box.click()

#video = browser.find_element(By.XPATH,"//input[@title='"+code+"']")
#video.click()
'''