import requests
import tweepy
from selenium.webdriver.common.by import By
import config
import redditbot
import browser_init
import sys

client = tweepy.Client(bearer_token=config.BEARER_TOKEN,
                       consumer_key=config.API_KEY,
                       consumer_secret=config.API_KEY_SECRET,
                       access_token=config.ACCESS_TOKEN,
                       access_token_secret=config.ACCESS_TOKEN_SECRET,
                       return_type=requests.Response,
                       wait_on_rate_limit=True)


def tweet(args=None):
    '''
    Browses Website for videos and tweets links of them
    '''
    codes_dict = redditbot.Main(args)
    codes = list(codes_dict.keys())
    browser = browser_init.init_browser()
    if browser is not None:
        browser.get("https://www.javlibrary.com/en/")
        try:
            warning = browser.find_element(By.XPATH, "//input[@type='button' and @value='I agree.']")
            warning.click()
        except:
            print("No Confirmation needed")
        for code in codes:
            if not 'www.javlibrary.com' in browser.current_url:
                browser.close()
            try:
                search_box = browser.find_element(By.ID, 'idsearchbox')
                search_box.send_keys(code)
                search_box = browser.find_element(By.ID, 'idsearchbutton')
                search_box.click()
            except:
                print("No ID Searchbox")
            try:
                video = browser.find_element(By.XPATH, "//div[text()='" + code + "']")
                video.click()
            except:
                print("Code directly after search")
            try:
                url = browser.current_url
                client.create_tweet(text=url)
                print("tweet")
            except:
                print("No Tweet")
    print("Success Twitter")

if __name__ == '__main__':
    tweet(sys.argv)