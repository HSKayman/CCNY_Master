import tweepy
from textblob import TextBlob

consumer_key = 'CONSUMER_KEY'
consumer_secret = 'CONSUMER_SECRET'
access_token = 'ACCESS_TOKEN'
access_token_secret = 'ACCESS_TOKEN_SECRET'

# Authenticate with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Fetch tweets
tweets = api.search_tweets(q="Python Programming", lang="en", count=100)

# Analyze sentiment
for tweet in tweets:
    analysis = TextBlob(tweet.text)
    sentiment = "Positive" if analysis.sentiment.polarity > 0 else "Negative"
    print(f"Tweet: {tweet.text}\nSentiment: {sentiment}\n")

