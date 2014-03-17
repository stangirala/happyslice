import ConfigParser
import json
from collections import namedtuple
import matplotlib.pyplot as plt

import sample_twitter
import parser


words_base = namedtuple("words_base", ["word", "pos_tag"], verbose=False)
class words(words_base):
    def __new__(cls, word, pos_tag):
        obj = words_base.__new__(cls, word, pos_tag)
        return obj

scores = namedtuple("scores", ["pos", "neg"], verbose=False)

def readSentimentFile():
    ''' Has file specific indexes. '''

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

def main(keywords, words_dict=None):

    if words_dict is None:
        words_dict = readSentimentFile()

    ''' Sample twitter. Uses a conf file. '''
    sample_twitter.sampleTwitter(keywords)

    ''' Tag lines and generate scores. '''
    sample = open('twitter_sample.txt', 'r')
    vals = []
    for line in sample:
        tweetjson = json.loads(line)
        print tweetjson['text'], tweetjson['base_sentiment']
        pos_tags = parser.posTag(tweetjson['text'])

        base = tweetjson['base_sentiment']
        if base == 'HAPPY':
            sentence_mean = 1
        elif base == 'SAD':
            sentence_mean = -1
        elif base == 'SURPRISE':
            sentence_mean = 0.5
        else:
            sentence_mean = 0

        for pair in pos_tags:
            word_key = words(pair[0], pair[1])
            if word_key in words_dict:
                score = words_dict[word_key]
                sentence_mean += float(score.pos) - float(score.neg)

        print 'Sentiment: ', sentence_mean
        vals.append(sentence_mean)

    sample.close()

    ''' Plot distribution. '''
    return vals


if __name__ == '__main__':

    data = main(raw_input('Keywords to track (Enter to random sample tweets): '))

    ''' Plot distribution. '''
    plt.hist(data)
    plt.show()
