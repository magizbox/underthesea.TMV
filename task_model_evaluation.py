# -*- coding: utf-8 -*-
from datetime import datetime
import io
from gensim.models import Word2Vec
import itertools


def log(s):
    print s
    s = unicode(s) + u"\n"
    f.write(s)


log_file = "logs\\%s-word-analogies.txt" % datetime.now().strftime('%Y-%m-%d_%H-%M')
f = io.open(log_file, "w", encoding="utf-8")

# analogy task
model = Word2Vec.load("model\\word2vec.model")
lines = open("question-words.txt").read().decode("utf-8").splitlines()
lines = [line.split("\t") for line in lines]


def first_character(word):
    try:
        return word[0]
    except:
        return ""


groups = []

log_file = "logs\\%s-vocab.txt" % datetime.now().strftime('%Y-%m-%d_%H-%M')
vocab_file = io.open(log_file, "w", encoding="utf8")
words = sorted(model.wv.vocab.keys())
for k, g in itertools.groupby(words, first_character):
    content = "[" + k + "]" + "\n"
    content += u", ".join(list(g)) + "\n\n"
    vocab_file.writelines(content)
score = 0
total = len(lines)
for line in lines:
    if line[0] == "":
        continue
    if ":" in line[0]:
        log("\n")
        log(line[0])
        continue
    try:
        w1, w2, w3, w4 = line
        result = model.wv.most_similar(positive=[w1, w2], negative=[w3])
        similar_words = [item[0] for item in result]
        if w4 == similar_words[0]:
            score += 1
            result = u"[✓] "
        else:
            result = u"[ ] "
        line = result + u", ".join([w1, w2, w3]) + " => " + similar_words[0] + u" (%s), " % w4 + u", ".join(
            similar_words[1:])
        log(line)
    except Exception, e:
        print e
        print "Cannot find similar for", u", ".join([w1, w2, w3, w4])
final_result = u"Final Result: %s / %s" % (score, total)
log(final_result)