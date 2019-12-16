import os
import tweepy

from shift_code_scraper.stream_listener import ShiftCodeStreamListener

print("Starting scraper", flush=True)
auth = tweepy.OAuthHandler(os.environ['TWITTER_APP_KEY'], os.environ['TWITTER_APP_SECRET'])
auth.set_access_token(os.environ['TWITTER_KEY'], os.environ['TWITTER_SECRET'])

api = tweepy.API(auth)

stream_listener = ShiftCodeStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(follow=["906234810"]) #dgSHiFTCodes
# stream.filter(follow=["1184299643909353472"]) #me

