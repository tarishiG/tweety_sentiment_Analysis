from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob

# import twitter keys and tokens
import twitter_crenditials
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

### Twitter Client ###
class TwitterClient():
    def __init__(self,twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client= API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self,num_tweets):
        tweets =[]
        for tweet in Cursor(self.twitter_client.user_timeline,id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets
    def get_frn_list(self,num_frns):
        frn_list =[]
        for frn in Cursor(self.twitter_client.friends,id=self.twitter_user).items(num_frns):
            frn_list.append(frn)
        return frn_list
    def get_home_timeline_tweets(self,num_tweets):
        home_tweets =[]
        for tweet in Cursor(self.twitter_client.home_timeline,id=self.twitter_user).items(num_tweets):
            home_tweets.append(tweet)
        return home_tweets



### Twitter Authenticator ###
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        # set twitter keys/tokens
        auth = OAuthHandler(twitter_crenditials.consumerKey, twitter_crenditials.consumerKey_secret)
        auth.set_access_token(twitter_crenditials.access_token, twitter_crenditials.access_tockenSeceret)
        return auth

### Twitter Srtreamer ###
class TwitterStreamer():
    """
    Class for streaming nad processing live tweets
    """
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()


    def stream_tweets(self, fetched_tweets, hashtag_list):
#Handling authentication and Connection to Tweeter API

# create instance of the tweepy tweet stream listener

        listener = TwitterListener(fetched_tweets)
        auth= self.twitter_authenticator.authenticate_twitter_app()

# create instance of the tweepy stream
        stream = Stream(auth, listener)

# search twitter for keyword
        stream.filter(track=hashtag_list)


### Twitter StreamListener ###
class TwitterListener(StreamListener):
  """
  Standard listner : prints fetched tweets on stdout
  """
  def __init__(self, fetched_tweets):
      self.fetched_tweets = fetched_tweets
#On success
  def on_data(self, data):
      try:
          print(data)
          with open(self.fetched_tweets,'a')as tf:
              tf.write(data)
              return True
      except BaseException as e:
          print("Error: %s"%str(e))
          return True
  #on_failure
  def on_error(self, status):
      if status==420:
          # Returning False on_data method in case rate limit occurs.
          return False
      print(status)

### Tweet Analyzer ###

class TweetAnalyzer():
    """
    Functionaly for analyzing and categorizing content from tweets.
    """

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def sentiment_analysis(self,tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity== 0:
            return 0
        else:
            return -1

    def tweets_to_dataFrame(self,tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets],columns=['tweets'])
        df['id']= np.array([tweet.id for tweet in tweets])
        df['len']= np.array([len(tweet.text) for tweet in tweets])
        df['date']= np.array([tweet.created_at for tweet in tweets])
        df['source']= np.array([tweet.source for tweet in tweets])
        df['likes']= np.array([tweet.favorite_count for tweet in tweets])
        df['retweet']= np.array([tweet.retweet_count for tweet in tweets])
        return df

if __name__ == '__main__':

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name= "Bees_Kut",count=200)
    df = tweet_analyzer.tweets_to_dataFrame(tweets)
    df['sentiments']= np.array([tweet_analyzer.sentiment_analysis(tweet) for tweet in df['tweets']])
    print(df.head(10))



"""""
  Numpy Trends
  
    # Avg length over all tweets
    print(np.mean(df['len']))

    # Most liked tweet
    print(np.max(df['likes']))

    # Most retweeted tweet.
    print(np.max(df['retweet']))

Data visualization

    # Time Series Data visualization
    time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    time_likes.plot(figsize=(18,5),label="Likes", legend = True)
    time_retweets = pd.Series(data=df['retweet'].values, index=df['date'])
    time_retweets.plot(figsize=(18, 5), label="Retweets", legend=True)
    plt.show()
"""""












