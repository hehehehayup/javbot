from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os


def init_browser():
    '''
    Initializes Chrome Browser with certain settings and returns it

    Returns
    -------
    drive: webdriver.chrome
    '''
    options = Options()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    idk = os.environ.get("CHROMEDRIVER_PATH")
    service = Service(idk)
    try:
        driver = webdriver.Chrome(service=service, options=options)
    except:
        print("Browser could be initialized")
    return driver