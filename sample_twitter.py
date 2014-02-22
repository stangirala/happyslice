from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import ConfigParser
import json
import re

def baseSentiment(text):

    ''' Adapted from https://github.com/aritter/twitter_nlp/blob/master/python/emoticons.py
        Regexps to handle emoticons. '''

    mycompile = lambda pat:  re.compile(pat,  re.UNICODE)

    NormalEyes = r'[;:=]'

    NoseArea = r'(|o|O|-)'   ## rather tight precision, \S might be reasonable...

    HappyMouths = r'[}pPD\)\]]'
    SadMouths = r'[{\(\[]'
    OtherMouths = r'[doO/\\]'  # remove forward slash if http://'s aren't cleaned

    Happy_RE =  mycompile( '(\^_\^|' + NormalEyes + NoseArea + HappyMouths + ')')
    Sad_RE = mycompile(NormalEyes + NoseArea + SadMouths)
    Surprise_RE = mycompile(NormalEyes + NoseArea + OtherMouths)

    #Emoticon = ("("+NormalEyes+"|"+Wink+")" + NoseArea + "("+Tongue+"|"+OtherMouths+"|"+SadMouths+"|"+HappyMouths+")")
    #Emoticon_RE = mycompile(Emoticon)

    h = Happy_RE.search(text)
    s = Sad_RE.search(text)
    n = Surprise_RE.search(text)
    if h and s: return "BOTH_HS"
    if h: return "HAPPY"
    if s: return "SAD"
    if n: return "SURPRISE"
    return "NA"

def cleanText(text):

    ''' Removes RT, Mentions and urls. '''

    check_string = 'abcdefghijklmnopqrstuvwxyz'

    tokens = text.split()
    clean_tokens = []
    for token in tokens:
        if token[0] != '#' and token[0] != '\\' and token[0] != '@' and '/' not in token and 'RT' not in token:
            for i in token:
                if i in check_string:
                    clean_tokens.append(token)

    print ' '.join(i for i in clean_tokens)

    return clean_tokens

class SampleStreamListener(StreamListener):

    count = 0

    def on_data(self, data):

        if self.count < 100:
            tweet = json.loads(data)
            if 'text' in tweet:
                text = tweet['text']
                clean_tokens = cleanText(text)
                if len(clean_tokens) > 0:
                    print 'Getting Tweet #'+str(self.count+1)
                    sample = open('twitter_sample.txt', 'a')
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
    key_list = ['consumer_key', 'consumer_secret', 'token_key', 'token_secret']
    con_key = config.get(section, 'consumer_key')
    con_secret = config.get(section, 'consumer_secret')
    token_key = config.get(section, 'token_key')
    token_secret = config.get(section, 'token_secret')

    listener = SampleStreamListener()
    auth = OAuthHandler(con_key, con_secret)
    auth.set_access_token(token_key, token_secret)

    stream = Stream(auth, listener)
    stream.sample()