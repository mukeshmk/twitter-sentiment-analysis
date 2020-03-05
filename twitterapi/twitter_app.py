import tweepy
from config import *

# Creating the authentication object
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
# Setting your access token and secret
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# Creating the API object while passing in auth information
api = tweepy.API(auth)

username = "nytimes"
tweetCount = 1

# Calling the user_timeline function with our parameters
results = api.user_timeline(id=username, count=tweetCount)

for tweet in results:
   print(tweet.text)
