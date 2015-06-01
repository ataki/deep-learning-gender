import os
import json
import csv
import pdb
import string
import errno

from operator import itemgetter
from collections import Counter

import cPickle as pickle

# Equivalent to mkdir -p
def mkdir_p(directory):
    try:
        os.mkdir(directory)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise e
        pass


def top_percentage_vocab(percentage):
    def extract(l):
        w, _, cnt = l
        return (w.strip(), float(cnt))

    result = []
    num = 0

    with open("data/class_vocab/vocab.ptb.txt") as f:
        reader = csv.reader(f, delimiter="\t")
        elems = dict([extract(l) for l in reader])
        freq_map = Counter(elems)

        num = int(len(freq_map) * percentage)
        top_n = freq_map.most_common(num)

        result = map(itemgetter(0), top_n)

    with open("data/class_vocab/vocab.txt") as vocab_f, \
        open("data/class_vocab/wordVectors.txt") as wV_f, \
        open("data/vocab/r.%s.vocab.txt" % num, "w") as vocab_out, \
        open("data/vocab/r.%s.wordVectors.txt" % num, "w") as wV_out, \
        open("data/vocab/r.%s.failed.txt" % num, "w") as failed_out:

        vocab_lines = [x.strip() for x in vocab_f]
        wordvec_lines = [v.strip() for v in wV_f]

        mirror = lambda x: (x[1], x[0])
        vocab_line_dict = dict(map(mirror, enumerate(vocab_lines)))

        count = 0
        failed = 0
        for word in result:
            if word in vocab_line_dict:
                index = vocab_line_dict[word]
                vocab_out.write(word + "\n")
                wV_out.write(wordvec_lines[index] + "\n")
                count += 1
            else:
                failed_out.write(word + "\n")
                failed += 1

        print "Done! Wrote out %s. Failed %s" % (count, failed)

if __name__ == "__main__":
    mkdir_p("data/vocab")
    top_percentage_vocab(0.13)
