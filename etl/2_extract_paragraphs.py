#!/usr/bin/python

"""
Export into folders suitable for paragraphvec
training.
"""

import unicodecsv as csv
from pickle import Pickler, Unpickler
import sys
import os
import errno
import shutil
import codecs

# max length of numerically iterated file name
# e.g.
#   4 => "0001.txt", "0002.txt", ...
#   5 => "00001.txt", "00002.txt", ...
MAX_FILENAME_LEN = 4

# Equivalent to mkdir -p
def mkdir_p(directory):
    try:
        os.mkdir(directory)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise e
        pass

# Equivalent to rm -rf dir
def rm_rf(directory):
    try:
        shutil.rmtree(directory)
    except OSError, e:
        pass

# Split up single blog post into paragraphs.
# We denote paragraphs as ending with
# newlines.
def extract_phrases(doc):
    return doc.split("\n")

# Writes a set of sentences to text
def write_to_file(fname, phrase):
    if len(phrase) == 0:
        return

    f = codecs.open(fname, "w", encoding="utf-8")
    f.write(phrase)

# Generates filenames given an integer
# numeric counter. Left-fills based on the
# global constant MAX_FILENAME_LEN
def generate_filename(counter):
    global MAX_FILENAME_LEN

    l = MAX_FILENAME_LEN - len(str(counter))
    if l > 0:
        return ("0" * l) + str(counter) + ".txt"
    else:
        return str(counter) + ".txt"

############
# Start

#############
# Make directories

print "Making directories if not exists..."
rm_rf("./pos")
rm_rf("./neg")
rm_rf("./unlabeled")
mkdir_p("./pos")
mkdir_p("./neg")
mkdir_p("./unlabeled")
print "Done"

#############
# Output blog posts to directories

SOURCE = "./training.csv"

with open(SOURCE, "r") as fin:

    reader = csv.reader(fin, encoding="utf-8", delimiter="|")

    # Start at "0001.txt"
    p_counter = 1
    n_counter = 1
    u_counter = 1

    line_counter = 0
    for x in reader:
        line_counter += 1

        # Extract sentences
        doc = x[0]
        label = int(x[1])

        if label == 1:
            # Output doc to pos file dir
            phrases = extract_phrases(doc)
            for phrase in phrases:
                incr_filename = generate_filename(p_counter)
                success = write_to_file("./pos/" + incr_filename, phrase)
                p_counter += 1

        elif label == 0:
            # Output doc to neg file dir
            phrases = extract_phrases(doc)
            for phrase in phrases:
                incr_filename = generate_filename(n_counter)
                success = write_to_file("./neg/" + incr_filename, phrase)
                n_counter += 1

        else:
            # Other
            # Output doc to unlabeled file
            phrases = extract_phrases(doc)
            for phrase in phrases:
                incr_filename = generate_filename(u_counter)
                success = write_to_file("./unlabeled/" + incr_filename, phrase)
                u_counter += 1

    print "lines: ", str(line_counter)
