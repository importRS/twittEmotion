import uuid
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import re
import os
from dotenv import load_dotenv

image_name = ""
load_dotenv()

class TwitterClient(object):
    def __init__(self):
        # Twitter API credentials
        consumer_key = os.getenv('consumer_key')
        consumer_secret = os.getenv('consumer_secret')
        access_token =  os.getenv('access_token')
        access_token_secret =  os.getenv('access_token_secret')

        # authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    # removing hashtags,emojis,stopwords
    def clean_txt(self, txt):

        txt = txt.encode("ascii", "ignore")
        txt = txt.decode()
        txt = re.sub(r'@[A-Z0-9a-z:]+', '', txt)  # replace username-tags
        txt = re.sub(r'^[RT]+', '', txt)  # replace RT-tags
        txt = re.sub('https?://[A-Za-z0-9./]+', '', txt)  # replace URLs
        txt = re.sub("[^a-zA-Z]", " ", txt)  # replace hashtags
        # removing punctuation,numbers and whitespace
        res = re.sub(r'[^\w\s]', '', txt.lower())
        res = re.sub('\s+', ' ', res)
        return res

    def get_tweet_sentiment(self, tweet):
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_txt(tweet))
        # setting sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query):
        # Function to fetch tweets and parse them.
        # empty list to store parsed tweets

        try:
            # call twitter api to fetch tweets
            # Define the search term and the date_since date as variables
            tweets = []
            # Collect tweets
            fetched_tweets = tweepy.Cursor(self.api.search, q=query,
                                           lang="en").items(100)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                parsed_tweet['clean tweet'] = self.clean_txt(tweet.text)
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(
                    tweet.text)

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

# class ends
