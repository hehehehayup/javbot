import requests
import tweepy
from selenium.webdriver.common.by import By
import config
import redditbot
import web_scraper

client = tweepy.Client(bearer_token=config.BEARER_TOKEN,
                       consumer_key=config.API_KEY,
                       consumer_secret=config.API_KEY_SECRET,
                       access_token=config.ACCESS_TOKEN,
                       access_token_secret=config.ACCESS_TOKEN_SECRET,
                       return_type=requests.Response,
                       wait_on_rate_limit=True)


def tweet():
    '''
    Browses Website for videos and tweets links of them
    '''
    codes_dict = redditbot.Main()
    codes = list(codes_dict.keys())
    browser = web_scraper.init_browser()
    browser.get("https://www.javlibrary.com/en/")
    for code in codes:
        if not 'www.javlibrary.com' in browser.current_url:
            browser.close()
        try:
            warning = browser.find_element(By.XPATH, "//input[@type='button' and @value='I agree.']")
            warning.click()
        except Exception:
            print("No Confirmation needed")
        try:
            search_box = browser.find_element(By.ID, 'idsearchbox')
            search_box.send_keys(code)
            search_box = browser.find_element(By.ID, 'idsearchbutton')
            search_box.click()
        except Exception:
            print("No ID Searchbox")
        try:
            video = browser.find_element(By.XPATH, "//div[text()='" + code + "']")
            video.click()
        except Exception:
            print("Code directly after search")
        url = browser.current_url
        client.create_tweet(text=url)
    print("Success Twitter")

if __name__ == '__main__':
    tweet()