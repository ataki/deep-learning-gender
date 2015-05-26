import pytumblr
import model
import tokenizer
import os

ENV = os.environ

### Wrap api into common module

class Client(object):
    def __init__(self):
        self.client = pytumblr.TumblrRestClient(
            ENV['TUMBLR_CONSUMER_KEY'],
            ENV['TUMBLR_CONSUMER_SECRET'],
            ENV['TUMBLR_OAUTH_TOKEN'],
            ENV['TUMBLR_OAUTH_SECRET'],
        )

    def get_posts(self):
        terms = ['fashion', 'action', 'movies', 'apple', 
            'stock', 'obama', 'campaign', 'food',
            'starcraft', 'loreal'] 

        accum = []
        before = 0
        for term in terms:
            posts = self.client.tagged(term, before=before, limit=20, 
                filter='text')
            accum.append(map(self.to_sql_row, posts))
        return accum

    def to_sql_row(self, result):
        post = result['body']
        blogname = result['blog_name']
        post_id = result['id']
        timestamp = result['date']
        return {
            'post': " ".join(tokenize(post)),
            'blogname': blogname,
            'post_id': post_id,
            'gender': gender,
            'timestamp': timestamp
        }