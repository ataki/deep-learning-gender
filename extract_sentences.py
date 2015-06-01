import unicodecsv as csv
from pickle import Pickler, Unpickler
import sys
import os
import errno
import shutil
import string
import re
import pdb

# Data directory to write out to
DATA_DIR = "data/blog"

# Raw data source
SOURCE = "data/training.csv"

# Data Vocab Source
VOCAB_SOURCE = "data/vocab/r.4997.vocab.txt"

# Number of sentences that comprise a paragraph
K = 40

# Max digits for training examples' filenames
MAX_FILENAME_LEN = 4

def get_vocab_set():
    with open(VOCAB_SOURCE) as f:
        return set([x.strip() for x in f])

vocab_set = get_vocab_set()

# Given relative path, resolves full data path
def get_data_path(dirname):
    return os.path.join(DATA_DIR, dirname)

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


# Sanitize each sentence to map to a
# vocab our neural net implementation
# can recognize
def clean_word(word):
    global vocab_set

    if word not in vocab_set:
        return "UUUNKKK"
    else:
        return word


def only_ascii(char):
    if ord(char) == 32:
        return char
    elif ord(char) < 48 or ord(char) > 127:
        return ''
    else:
        return char


# Split up single blog post into sentences, then
# get a K run of sentences
def extract_phrases(doc):
    global K
    in_ascii = filter(only_ascii, doc)
    doc = str(in_ascii).translate(string.maketrans("",""), string.punctuation)
    doc = re.sub("\d", " DG ", doc)

    # Finish doc processing; now do words
    words = map(clean_word, doc.lower().split(" "))
    paginated_lines = []

    for s in range(0, len(words), K):
        next_k_words = words[s:s+K]
        phrase = " ".join(next_k_words)
        paginated_lines.append(phrase.strip())
    return paginated_lines


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

# Writes a set of sentences to text
def write_to_file(fname, phrase):
    if len(phrase) == 0:
        return

    # f = codecs.open(fname, "w", encoding="utf-8")
    f = open(fname, "w")
    f.write(phrase)

if __name__ == "__main__":
    rm_rf(get_data_path("pos"))
    rm_rf(get_data_path("neg"))
    rm_rf(get_data_path("unlabeled"))

    mkdir_p(get_data_path("pos"))
    mkdir_p(get_data_path("neg"))
    mkdir_p(get_data_path("unlabeled"))

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
                    success = write_to_file(get_data_path("pos") + "/" + incr_filename, phrase)
                    p_counter += 1

            elif label == 0:
                # Output doc to neg file dir
                phrases = extract_phrases(doc)
                for phrase in phrases:
                    incr_filename = generate_filename(n_counter)
                    success = write_to_file(get_data_path("neg") + "/" + incr_filename, phrase)
                    n_counter += 1

            else:
                # Other
                # Output doc to unlabeled file
                phrases = extract_phrases(doc)
                for phrase in phrases:
                    incr_filename = generate_filename(u_counter)
                    success = write_to_file(get_data_path("unlabeled") + "/" + incr_filename, phrase)
                    u_counter += 1

        print "lines: ", str(line_counter)
