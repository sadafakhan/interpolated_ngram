import os
import sys
import nltk

sentences = open(os.path.join(os.path.dirname(__file__), sys.argv[1]), 'r').read().split("\n")[:-1]

unigrams = {}
bigrams = {}
trigrams = {}

for sentence in sentences:
    sentence = nltk.word_tokenize(sentence)

    # add BOS/EOS markers
    sentence.insert(0, '<s>')
    sentence.append('</s>')

    # build unigrams
    for word in sentence:
        if word not in unigrams:
            unigrams[word] = 1
        else:
            unigrams[word] += 1

    # build bigrams
    for i in range(len(sentence)):
        if i == (len(sentence)-1):
            pass
        else:
            bigram = sentence[i] + " " + sentence[i+1]
            if bigram not in bigrams:
                bigrams[bigram] = 1
            else:
                bigrams[bigram] += 1

    # build trigrams
    for i in range(len(sentence)-1):
        if i == (len(sentence)-2):
            pass
        else:
            trigram = sentence[i] + " " + sentence[i+1] + " " + sentence[i+2]
            if trigram not in trigrams:
                trigrams[trigram] = 1
            else:
                trigrams[trigram] += 1


sorted_unigrams = [(k, v) for k, v in sorted(unigrams.items(), key=lambda x: x[1], reverse=True)]
sorted_bigrams = [(k, v) for k, v in sorted(bigrams.items(), key=lambda x: x[1], reverse=True)]
sorted_trigrams = [(k, v) for k, v in sorted(trigrams.items(), key=lambda x: x[1], reverse=True)]


with open(sys.argv[2], 'w', encoding='utf8') as g:
    for unigram in sorted_unigrams:
        g.write(str(unigram[1]) + "\t" + unigram[0] + "\n")
    for bigram in sorted_bigrams:
        g.write(str(bigram[1]) + "\t" + str(bigram[0]) + "\n")
    for trigram in sorted_trigrams:
        g.write(str(trigram[1]) + "\t" + str(trigram[0]) + "\n")