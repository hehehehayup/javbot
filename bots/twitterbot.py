import requests
import tweepy
import config
import redditbot

client = tweepy.Client(bearer_token=config.BEARER_TOKEN,
                       consumer_key=config.API_KEY,
                       consumer_secret=config.API_KEY_SECRET,
                       access_token=config.ACCESS_TOKEN,
                       access_token_secret=config.ACCESS_TOKEN_SECRET,
                       return_type=requests.Response,
                       wait_on_rate_limit=True)


