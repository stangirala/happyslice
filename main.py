from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import ConfigParser
import json
from collections import namedtuple

words_base = namedtuple("words_base", ["word", "pos_tag"], verbose=False)
class words(words_base):
    def __new__(cls, word, pos_tag):
        obj = words_base.__new__(cls, word, pos_tag)
        return obj

scores = namedtuple("scores", ["pos", "neg"], verbose=False)

def readSentimentFile():

    file_name = 'SentiWordNet_3.0.0_20130122.txt'
    sentimentfile = open(file_name, 'r')

    print 'Reading data file.'
    word_dict = {}
    for line in sentimentfile:
        if (line[0] != '#' and len(line.strip()) > 4):
            tokens = line.split()
            pos_tag = tokens[0]
            word_id = tokens[1]
            pos = tokens[2]
            neg = tokens[3]
            i = 4
            while tokens[i][len(tokens[i])-2] == '#':
                word = tokens[i].split('#')[0]
                score_tuple = scores(pos, neg)
                word_key = words(word, pos_tag)
                word_dict[word_key] = score_tuple
                i += 1

    print 'Done reading data file.'

    return word_dict

class SampleStreamListener(StreamListener):

    count = 0

    def on_data(self, data):

        if self.count < 100:
            tweet = json.loads(data)
            if 'text' in tweet:
                print 'Getting Tweet #'+str(self.count)
                sample = open('twitter_sample.txt', 'w')
                #sample.write(tweet['text'].encode('utf-8')+'\n')
                sample.write(json.dumps(tweet)+'\n')
                self.count += 1
                sample.close()
            else:
                exit(0)
        return True

    def on_error(self, status):
        print "*******ERROR******", status
        exit(0)


def sampleTwitter():

    config = ConfigParser.ConfigParser()
    config.read('conf/config.file')
    section = 'Twitter'
    options = config.options(section)
    configdict = {}
    for option in options:
        configdict[option] = config.get(section, option)
    key_list = ['consumer_key', 'consumer_secret', 'token_key', 'token_secret']
    for key in key_list:
        if key not in configdict:
            print 'Bad config file.'
            return(-1)

    con_key = config.get(section, 'consumer_key')
    con_secret = config.get(section, 'consumer_secret')
    token_key = config.get(section, 'token_key')
    token_secret = config.get(section, 'token_secret')
    listener = SampleStreamListener()
    auth = OAuthHandler(con_key, con_secret)
    auth.set_access_token(token_key, token_secret)

    stream = Stream(auth, listener)
    stream.sample()


if __name__ == '__main__':

    '''words_dict = readSentimentFile()

    word_key = words("abducting", "a")
    score_tuple = words_dict[word_key]
    print score_tuple.pos, score_tuple.neg
    word_key = words("dissilient", "a")
    score_tuple = words_dict[word_key]
    print score_tuple.pos, score_tuple.neg'''

    ''' Sample twitter. Uses a conf file. '''
    sampleTwitter()

    ''' Tag lines. '''
    sample = open('twitter_sample.txt', 'r')
    for line in sample:
        tweetjson = json.loads(line)
        print tweetjson['Text']


    ''' Return sample sentiment. '''









