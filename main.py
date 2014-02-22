import sample_twitter
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

if __name__ == '__main__':

    '''words_dict = readSentimentFile()

    word_key = words("abducting", "a")
    score_tuple = words_dict[word_key]
    print score_tuple.pos, score_tuple.neg
    word_key = words("dissilient", "a")
    score_tuple = words_dict[word_key]
    print score_tuple.pos, score_tuple.neg'''

    ''' Sample twitter. Uses a conf file. '''
    sample_twitter.sampleTwitter()

    ''' Tag lines. '''
    sample = open('twitter_sample.txt', 'r')
    for line in sample:
        tweetjson = json.loads(line)
        #print tweetjson['Text']





    sample.close()


    ''' Return sample sentiment. '''









