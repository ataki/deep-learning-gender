#!/usr/bin/python

import tumblpy
import twitter
import sys
import os
import sqlite3
import models

ENV = os.environ

### Tumblr Client

t1 = tumblpy.Tumblpy(
    ENV['TUMBLR_CONSUMER_KEY'],
    ENV['TUMBLR_CONSUMER_SECRET']
)

auth_props = t1.get_authentication_tokens(callback_url='http://localhost:8000')
auth_url = auth_props['url']

OAUTH_TOKEN = auth_props['oauth_token']
OAUTH_TOKEN_SECRET = auth_props['oauth_token_secret']

print 'Connect with tumblr via: %s' % auth_url

t2 = tumblpy.Tumblpy(
    ENV['TUMBLR_CONSUMER_KEY'],
    ENV['TUMBLR_CONSUMER_SECRET'],
    OAUTH_TOKEN,
    OAUTH_TOKEN_SECRET
)

authorized_tokens = t2.get_authorized_tokens(oauth)

### Twitter Client

Twitter = twitter.Api(
    consumer_key=ENV['TWITTER_CONSUMER_KEY'],
    consumer_secret=ENV['TWITTER_CONSUMER_SECRET'],
    access_token_key=ENV['TWITTER_ACCESS_TOKEN'],
    access_token_secret=ENV['TWITTER_ACCESS_TOKEN']
)

# verify and continue

if api.VerifyCredentials():
    print "Twitter verification failed"
    sys.exit(1)

# fetch info into memory, async
# store into db


