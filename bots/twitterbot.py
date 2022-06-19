import requests
import tweepy
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
    codes_dict = redditbot.Main()
    codes = list(codes_dict.keys())
    for code in codes:
        website = 'https://www.javmost.com/' + code
        r = requests.get(website)
        if r.status_code != 404:
            try:
                client.create_tweet(text=website)
            except Exception:
                print("duplicate")
        else:
            browser = web_scraper.init_browser()
            browser.get("https://www.javlibrary.com/en/")

tweet()
