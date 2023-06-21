import math
import sys
import os
from nltk.tokenize import WhitespaceTokenizer

ngrams = open(os.path.join(os.path.dirname(__file__), sys.argv[1]), 'r').read().split("\n")[:-1]

# track types and tokens
uni_types = 0
uni_tokens = 0
bi_types = 0
bi_tokens = 0
tri_types = 0
tri_tokens = 0

for gram in ngrams:
    gram = WhitespaceTokenizer().tokenize(gram)
    if len(gram) == 2:
        uni_types += 1
        uni_tokens += int(gram[0])
    if len(gram) == 3:
        bi_types += 1
        bi_tokens += int(gram[0])
    if len(gram) == 4:
        tri_types += 1
        tri_tokens += int(gram[0])

# creates entries delineating ngram as key and a list with its respective probability and count as value
unigrams = {}
bigrams = {}
trigrams = {}

for gram in ngrams:
    gram = gram.split("\t")
    count = int(gram[0])
    actual_gram = gram[1]
    tokenized_gram = WhitespaceTokenizer().tokenize(gram[1])

    # unigrams
    if len(tokenized_gram) == 1:
        prob = count/uni_tokens
        unigrams[gram[1]] = [prob, count]

    # bigrams
    if len(tokenized_gram) == 2:
        w1 = tokenized_gram[0]
        prob = count/(unigrams[w1][1])
        bigrams[gram[1]] = [prob, count]

    # trigrams
    if len(tokenized_gram) == 3:
        w1w2 = ' '.join(word for word in tokenized_gram[0:2])
        prob = count/(bigrams[w1w2][1])
        trigrams[gram[1]] = [prob, count]

# actual string entries that will be outputted
uni_strings = []
bi_strings = []
tri_strings = []

# since we're iterating over a sorted file, we don't need to further sort; order is internally preserved
for gram in ngrams:
    gram = gram.split("\t")
    count = int(gram[0])
    actual_gram = gram[1]
    tokenized_gram = WhitespaceTokenizer().tokenize(gram[1])

    if len(tokenized_gram) == 1:
        prob = unigrams[actual_gram][0]
        count = unigrams[actual_gram][1]
        lgprob = math.log(prob, 10)
        entry = str(count) + " " + str(prob) + " " + str(lgprob) + " " + actual_gram + "\n"
        uni_strings.append(entry)

    if len(tokenized_gram) == 2:
        prob = bigrams[actual_gram][0]
        count = bigrams[actual_gram][1]
        lgprob = math.log(prob, 10)
        entry = str(count) + " " + str(prob) + " " + str(lgprob) + " " + actual_gram + "\n"
        bi_strings.append(entry)

    if len(tokenized_gram) == 3:
        prob = trigrams[actual_gram][0]
        count = trigrams[actual_gram][1]
        lgprob = math.log(prob, 10)
        entry = str(count) + " " + str(prob) + " " + str(lgprob) + " " + actual_gram + "\n"
        tri_strings.append(entry)


# write to file
with open(sys.argv[2], 'w', encoding='utf8') as g:
    g.write("\data\\\n")
    g.write("ngram 1: type=" + str(uni_types) + " token=" + str(uni_tokens) + "\n")
    g.write("ngram 2: type=" + str(bi_types) + " token=" + str(bi_tokens) + "\n")
    g.write("ngram 3: type=" + str(tri_types) + " token=" + str(tri_tokens) + "\n")
    g.write("\n")
    g.write("\\1-grams:\n")
    for entry in uni_strings:
        g.write(entry)
    g.write("\\2-grams:\n")
    for entry in bi_strings:
        g.write(entry)
    g.write("\\3-grams:\n")
    for entry in tri_strings:
        g.write(entry)
