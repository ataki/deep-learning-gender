#!/usr/bin/python

"""
Clean raw docs up a bit and map labels to {1, -1}.
Docs are encoded in utf-8, so don't assume ascii
when using any other libraries.
"""

import unicodecsv as csv
import json
from collections import Counter

SOURCE = "./raw/training-Table 1.csv"

TARGET = "./training.csv"

WORD_DIST_OUT = "./word-dist.csv"

c = Counter()

def extract_doc(doc):
    return doc

def extract_label(l):
	if len(l) == 0:
		return -1
	elif l.strip().upper() == "M":
		return 1
	else:
		return 0

with open(SOURCE, "r") as fin, open(TARGET, "w") as fout:
    reader = csv.reader(fin, encoding="utf-8")
    clean = []
    for x in reader:
    	doc = extract_doc(x[0])
    	label = extract_label(x[1])
    	c.update(doc)
    	clean.append((doc, label))
    writer = csv.writer(fout, encoding="utf-8", delimiter="|")
    for out_row in clean:
   		writer.writerow(out_row)

ffreq = open(WORD_DIST_OUT, "w")
ffreq.write(json.dumps(c))
ffreq.close()