import requests
import tweepy
import config
import redditbot
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os


client = tweepy.Client(bearer_token=config.BEARER_TOKEN,
                       consumer_key=config.API_KEY,
                       consumer_secret=config.API_KEY_SECRET,
                       access_token=config.ACCESS_TOKEN,
                       access_token_secret=config.ACCESS_TOKEN_SECRET,
                       return_type=requests.Response,
                       wait_on_rate_limit=True)

def tweet():
    codes_dict = redditbot.Main()
    codes = list(codes_dict.keys())

    service = Service(os.environ.get("CHROMEDRIVER_PATH"))
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=service, options= chrome_options)
    driver.get("https://www.javlibrary.com/en/")
    print(driver.page_source)

tweet()
