from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os

service = Service(os.environ.get("CHROMEDRIVER_PATH"))
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://www.javlibrary.com/en/")
print(driver.page_source)