#!/usr/bin/python

"""
Extract and output sentences into a file
"""

import unicodecsv as csv
from pickle import Pickler, Unpickler
import sys
import os
import errno

try:
    os.mkdir('./data')
except OSError, e:
    if e.errno != errno.EEXIST:
        raise e
    pass

SOURCE = "./training.csv"

TARGET = "./data/"

def extract_doc(doc):
	return doc.replace("\r\n", "")

def write_to_txt(f, sentence_set):
    count = 0
    for sentence_tuple in sentence_set:
        try:
            f.write(" ".join(sentence_tuple) + "\n")
        except:
            count += 1
            continue
    print str(count) + " sentences have utf-8 encodings out of " + str(len(sentence_set))

with open(SOURCE, "r") as fin, \
	open(TARGET + "m-sentences", "w") as m_out, \
	open(TARGET + "f-sentences", "w") as f_out:

    reader = csv.reader(fin, encoding="utf-8")

    male_sentences = set()
    female_sentences = set()
    for x in reader:
    	sys.stdout.write('.')
    	doc = extract_doc(x[0])
    	label = int(x[1])
    	entries = [tuple(x.split(" ")) for x in doc.split(".")]
    	if label == 1:
    		# Male
    		for e in entries:
    			male_sentences.add(e)
    	elif label == 0:
    		# Female
    		for e in entries:
    			female_sentences.add(e)
    	else:
    		# Other
    		continue

    write_to_txt(m_out, male_sentences)
    write_to_txt(f_out, female_sentences)
