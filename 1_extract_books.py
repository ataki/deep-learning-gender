from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from gutenberg.query import get_etexts
from gutenberg.query import get_metadata

from lib import model
from lib import gender
from lib.gutenberg_authors import readmetadata
import json

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

# Fetches author and save to cache if none exist
def fetch_authors():
    authors_path = "data/authors.json"
    if not os.path.isfile(authors_path):
        author_data = readmetadata()
        with open(author_data, "w") as outfile:
            data_as_arr = [x for x in author_data]
            outfile.write(json.dumps(data_as_arr))
    with open(authors_path) as infile:
        return json.loads(infile.read())

# Dasherizes stuff
def dasherize(title):
    return "-".join(title.split(" "))

# A subroutine for fetching authors
#   of a certain century. Several external
#   dependencies, including that src_dir is
#   a valid directory, and that the db exists
#   for writing books into.
#      
#   Authors must be an iterable, src_dir a 
#   path to a valid directory to write out to,
#   and century an integer.
def extract_subroutine(authors, src_dir, century):
    session = model.get_session()
    for author in authors:
        e_ids = get_etexts('author', author)
        print author
        counter = 0

        for e_id in e_ids:
            title = get_metadata('title', e_id)
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
            counter += 1

        print "committing %s books to file" % counter
        session.commit()
        counter = 0

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
    only_1800_authors = lambda x: 1800 <= x.get("authoryearofbirth", 0) <= 1900
    only_1900_authors = lambda x: 1900 <= x.get("authoryearofbirth", 0) <= 2000

    clean_author_data = filter(remove_empty_authors, author_data)

    authors_1800 = map(get_author_names, filter(only_1800_authors, clean_author_data))
    authors_1900 = map(get_author_names, filter(only_1900_authors, clean_author_data))

    authors_1800 = set(authors_1800)
    authors_1900 = set(authors_1900)

    print "making source directories for book raw text"
    mkdir_p(os.path.join(base_source_dir, "1800"))
    mkdir_p(os.path.join(base_source_dir, "1900"))
    print "done."

    print "extracting text"
    extract_subroutine(authors_1800, os.path.join(base_source_dir, "1800"), 1800)
    extract_subroutine(authors_1900, os.path.join(base_source_dir, "1900"), 1900)
    print "done."

    print "finished book extraction."