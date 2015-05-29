import json
from operator import itemgetter

f = open("data/authors.json")

author_data = json.loads(f.read())

