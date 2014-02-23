import nltk


def translateWordnetTags(pos):

    translated_pos = []

    for i in xrange(0, len(pos)):
        if pos[i][1].startswith('J'):
            tag = 'a'
        elif pos[i][1].startswith('V'):
            tag = 'v'
        elif pos[i][1].startswith('N'):
            tag = 'n'
        elif pos[i][1].startswith('R'):
            tag = 'r'
        else:
            tag = ''

        translated_pos.append((pos[i][0], tag))

    return translated_pos

def posTag(text):

    tokens = nltk.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    pos = translateWordnetTags(pos)

    return pos
