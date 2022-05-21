# IMPORT
import tweepy
import os
import CONFIG
import json
from feel_it import EmotionClassifier
from feel_it import SentimentClassifier
import datetime

# AUTHENTICATION
auth = tweepy.OAuthHandler(CONFIG.API_KEY, CONFIG.APY_SECRET_KEY)
auth.set_access_token(CONFIG.ACCESS_TOKEN, CONFIG.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

# LISTENER

class MyListener(tweepy.StreamingClient):

    tweets = []
    limit = 1
    
    # on data

    def on_data(self, raw_data):
        time = datetime.datetime.now()
        print(time.hour," - ",time.minute)

        data = json.loads(raw_data)
        print(data)

        self.tweets.append(data)

        if time.hour == 9:
            self.disconnect()

        json.dump(data, open('streaming_tweet.json', 'a'))

    # on error
    def on_errors(self, errors):
        print(errors)
        return super().on_errors(errors)

# ------------------------------------


stream_tweet = MyListener(CONFIG.BEARER_TOKEN)

# STREAM BY KEYWORDS
keyword = '#HarrysHouse -is:retweet'

stream_tweet.add_rules(tweepy.StreamRule(keyword))
stream_tweet.filter(expansions=["author_id"], tweet_fields=['created_at',  'lang', 'entities', 'geo',
                    'public_metrics'], user_fields=['location', 'verified', 'public_metrics', 'id', 'username', 'name'])


# for t in stream_tweet.tweets:
#     data = t.data
#     print("Text: ", data)
#     print()

# TODO
# [ ] analizzare il sentimento dei vari tweet nelle prime tre ore dall'uscita dell'album
