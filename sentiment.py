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
