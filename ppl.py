import math
import os
import sys
from nltk.tokenize import WhitespaceTokenizer

lm_raw = open(os.path.join(os.path.dirname(__file__), sys.argv[1]), 'r').read().split("\n")[:-1]
l1 = float(sys.argv[2])
l2 = float(sys.argv[3])
l3 = float(sys.argv[4])
sentences = open(os.path.join(os.path.dirname(__file__), sys.argv[5]), 'r').read().split("\n")[:-1]


lm = {}

# process the LM
for entry in lm_raw:
    entry = WhitespaceTokenizer().tokenize(entry)
    if len(entry) < 4:
        pass
    elif entry[0] == 'ngram':
        pass
    else:
        count = float(entry[0])
        prob = float(entry[1])
        lgprob = float(entry[2])
        gram = ' '.join(word for word in entry[3:])
        lm[gram] = [count, prob, lgprob]

# initiate counters
sum = 0
word_num = 0
oov_num = 0
sent_num = len(sentences)
sentence_counter = 1

# process sentences
with open(sys.argv[6], 'w', encoding='utf8') as g:
    for sentence in sentences:
        g.write("Sent #" + str(sentence_counter) + ": <s> " + sentence + " </s>\n")
        sentence_counter += 1

        # initiate local counters
        local_sum = 0
        local_oov = 0

        # add BOS and EOS to sentences again
        sentence = WhitespaceTokenizer().tokenize(sentence)
        sentence.insert(0, '<s>')
        sentence.append('</s>')
        word_num += (len(sentence) - 2)


        # begin iterating through the words
        for w_i in range(len(sentence)):

            # skip BOS
            if sentence[w_i] == '<s>':
                pass


            else:
                # if wi is known (i.e., wi; appears in the lm_file)
                if sentence[w_i] in lm:
                    # due to passing the BOS marker, we always start from the second element
                    # we can't have a trigram in this case
                    if w_i == 1:
                        prob3 = 0

                    else:
                        tri = ' '.join(word for word in sentence[w_i-2:w_i+1])
                        if tri in lm:
                            prob3 = lm[tri][1]
                        else:
                            prob3 = 0

                    # but we can always have a bigram
                    bi = ' '.join(word for word in sentence[w_i-1:w_i+1])
                    if bi in lm:
                        prob2 = lm[bi][1]
                    else:
                        prob2 = 0


                    uni = sentence[w_i]
                    prob1 = lm[uni][1]

                    w_i_prob = math.log((l3 * prob3) + (l2 * prob2) + (l1 * prob1), 10)
                    local_sum += w_i_prob
                    sum += w_i_prob

                else:
                    # skip oov words
                    oov_num += 1
                    local_oov += 1
                    w_i_prob = 0

                if w_i_prob == 0:
                    g.write(str(w_i) + ": lg P(" + sentence[w_i] + " | " + sentence[w_i-1] + ") = -inf (unknown word)\n")
                elif prob3 == 0 and prob2 == 0:
                    g.write(str(w_i) + ": lg P(" + uni + " | " + sentence[w_i-2] + " " + sentence[w_i-1] + ") = " + str(w_i_prob)
                            + " (unseen ngrams)\n")
                else:
                    g.write(str(w_i) + ": lg P(" + uni + " | " + sentence[w_i-2] + " " + sentence[w_i-1] + ") = " + str(w_i_prob)
                            + "\n")

        g.write("1 sentence, " + str(len(sentence) - 2) + " words, " + str(local_oov) + " OOVs\n")

        local_cnt = len(sentence) - 2 - local_oov
        if local_cnt == 0:
            local_cnt = len(sentence) - 2
        local_total = -local_sum/local_cnt
        local_ppl = 10 ** local_total

        g.write("lgprob= " + str(local_sum) + " ppl= " + str(local_ppl) +  "\n\n\n\n")

    cnt = word_num + sent_num - oov_num
    total = -sum/cnt
    ppl = 10 ** total

    g.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
    g.write("sent_num=" + str(sent_num) + " word_num=" + str(word_num) + " oov_num=" + str(oov_num) + "\n")
    g.write("lgprob= " + str(sum) + " ave_lgprob=" + str(total) + " ppl=" + str(ppl) + "\n")



