from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from gutenberg.query import get_etexts
from gutenberg.query import get_metadata

from lib import model
from lib import gender
from lib.gutenberg_authors import readmetadata
import requests
import json

import time

import os
import errno

# Equivalent to mkdir -p
def mkdir_p(directory):
    try:
        os.mkdir(directory)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise e
        pass

mkdir_p("./logs")

import logging
logging.basicConfig(filename='logs/extract_books.log', filemode='w', level=logging.NOTSET,
    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
log = logging.getLogger("extract_books")

# Fetches author and save to cache if none exist
def fetch_authors():
    authors_path = "data/authors.json"
    if not os.path.isfile(authors_path):
        author_data = readmetadata()
        with open(authors_path, "w") as outfile:
            data_as_arr = [x for x in author_data]
            outfile.write(json.dumps(data_as_arr))
    with open(authors_path) as infile:
        return json.loads(infile.read())


# Dasherizes stuff
def dasherize(title):
    return "-".join(title.split(" "))


# Book extraction subroutine
#   Makes a request to Gutenberg API.
#   Susceptible to getting blocked.
def extract_book_contents(metadata):
    fmts = metadata.get('formats')
    if fmts is None:
        return None
    url = fmts.get('text/plain')
    if url is None:
        return None

    res = requests.get(url, verify=False)

    if res.status_code != requests.codes.ok:
        log.error("Couldn't download " + metadata['title'])
    else:
        contents = res.text
        lines = contents.split("\r\n")
        idx = -1
        import pdb
        pdb.set_trace()
        for i, l in enumerate(lines):
            if 'START OF THIS PROJECT' in l:
                idx = i
                break
        if idx != -1:
            return "\r\n".join(lines[:idx])
        else:
            log.error("Error parsing " + metadata['title'])
    return None

# A subroutine for fetching authors
#   of a certain century. Several external
#   dependencies, including that src_dir is
#   a valid directory, and that the db exists
#   for writing books into.
#
#   Authors must be an iterable, src_dir a
#   path to a valid directory to write out to,
#   and century an integer.
def extract_subroutine(data, src_dir, century):
    session = model.get_session()
    backoff = 1

    counter = 0
    for metadata in data:
        contents = extract_book_contents(metadata)

        if contents is None:
            backoff *= 1.5
            continue

        title = metadata['title']
        author = metadata['author']
        e_id = metadata['id']

        if type(title) == list:
            title = dasherize(title)

        text_file_path = os.path.join(src_dir, dasherize(title.split(" ")))
        text = strip_headers(load_etext(e_id)).strip()
        f = open(text_file_path, "w")
        f.write(text)
        f.close()
        book = model.Book(
            title=title,
            author=author,
            e_id=e_id,
            century=century,
            text_file_path=text_file_path
        )
        session.add(book)
        session.commit()
        log.info("successfully added " + title)
        counter += 1
        time.sleep(backoff)

    log.info("---- finished run. added %d books ----" % counter)

if __name__ == "__main__":
    base_source_dir = "data/books"

    print "making data dir"
    mkdir_p(base_source_dir)
    print "done."

    print "fetching authors"
    author_data = fetch_authors()
    print "done."

    ### Authors List to query
    # Each entry should be in the format
    # (first, last)

    get_author_names = lambda x: x['author']
    remove_empty_authors = lambda x: x['author'] is not None
    remove_english_books = lambda x: "en" in x['language']

    only_1800_authors = lambda x: 1800 <= x.get("authoryearofbirth", 0) <= 1900
    only_1900_authors = lambda x: 1900 <= x.get("authoryearofbirth", 0) <= 2000

    clean_author_data = filter(remove_english_books, filter(remove_empty_authors, author_data))

    authors_1800 = filter(only_1800_authors, clean_author_data)
    authors_1900 = filter(only_1900_authors, clean_author_data)

    print "making source directories for book raw text"
    mkdir_p(os.path.join(base_source_dir, "1800"))
    mkdir_p(os.path.join(base_source_dir, "1900"))
    print "done."

    print "extracting text"
    extract_subroutine(authors_1800, os.path.join(base_source_dir, "1800"), 1800)
    extract_subroutine(authors_1900, os.path.join(base_source_dir, "1900"), 1900)
    print "done."

    print "finished book extraction."
