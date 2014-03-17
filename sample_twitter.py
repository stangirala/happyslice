from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import ConfigParser
import json
import re
import os

import sentiment


def cleanText(text):

    ''' Removes RT, Mentions and urls. '''

    check_string = 'abcdefghijklmnopqrstuvwxyz'

    tweet = {}

    tweet['base_sentiment'] = sentiment.baseSentiment(text)

    tokens = text.split()
    clean_tokens = []
    for token in tokens:
        check = False
        if token[0] != '#' and token[0] != '\\' and token[0] != '@' and '/' not in token and 'RT' not in token:
            for i in token:
                if i not in check_string:
                    check = False
                    break
                else:
                    check = True
        if check == True:
            clean_tokens.append(token)

    tweet['text'] = ' '.join(i for i in clean_tokens)

    return tweet

class SampleStreamListener(StreamListener):

    count = 0
    max_count = 200

    def on_data(self, data):

        if self.count < self.max_count:
            tweet = json.loads(data)
            if 'text' in tweet and tweet['lang'] == 'en':
                text = tweet['text']
                clean_tweet = cleanText(text)
                if len(clean_tweet['text']) > 0:
                    print 'Getting Tweet #'+str(self.count+1)
                    sample = open('twitter_sample.txt', 'a')
                    sample.write(json.dumps(clean_tweet)+'\n')
                    self.count += 1
                    sample.close()
        else:
            return False

        return True

    def on_error(self, status):
        print "*******TWEEPY ERROR******", status
        exit(0)

def sampleTwitter(keywords):

    config = ConfigParser.ConfigParser()
    config.read('conf/config.file')
    section = 'Twitter'
    con_key = config.get(section, 'consumer_key')
    con_secret = config.get(section, 'consumer_secret')
    token_key = config.get(section, 'token_key')
    token_secret = config.get(section, 'token_secret')

    listener = SampleStreamListener()
    auth = OAuthHandler(con_key, con_secret)
    auth.set_access_token(token_key, token_secret)

    stream = Stream(auth, listener)

    if len(keywords) == 0:
        stream.sample()
    else:
        stream.filter(None, [i.strip() for i in keywords.split()])

    print 'DONE READING SAMPLE TWITTER'

