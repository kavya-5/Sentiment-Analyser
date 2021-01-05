import pickle
import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS
class TwitterClient(object):
    def __init__(self):
        consumer_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        consumer_secret = 'xxxxxxxxxxxxxxxxxxxxxxx'
        access_token = 'xxxxxxxxxxxxxxxxxxxxxxxxx'
        access_token_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxx'
        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 
  
    def clean_tweet(self, tweet): 
        cleantweet= ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
        return cleantweet
    def get_tweet_sentiment(self, tweet): 
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity < 0: 
            return 'negative'
        else: 
            return 'neutral'
    def get_tweets(self, query, count = 500):
        tweets=[]
        try:
            fetched_tweets = self.api.search(q = query, count = count)
            for tweet in fetched_tweets:  
                parsed_tweet = {} 
                parsed_tweet['text'] = tweet.text 
                
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
  
                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
  
            # return parsed tweets 
            return tweets 
        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e))
class Out():
    def output(self,query,n): 
      # creating object of TwitterClient Class 
      api = TwitterClient() 
      # calling function to get tweets
      tweets = api.get_tweets(query, count = 500) 
      self.ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 

      self.ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
      self.neutralt=[tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
    
      self.postweet=100*len(self.ptweets)/len(tweets)
      self.neutweet=100*len(self.neutralt)/len(tweets)
      self.negtweet=100*len(self.ntweets)/len(tweets)
      fig,ax=plt.subplots()
      sentiments=["positive","neutral","negative"]
      values=[self.postweet,self.neutweet,self.negtweet]
      ax.bar(sentiments,values,color=["green","yellow","red"])
      plt.savefig('templates/g1.png')
