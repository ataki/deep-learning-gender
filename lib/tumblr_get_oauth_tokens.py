import tumblpy
import urllib

# First step

ENV = os.environ

t1 = tumblpy.Tumblpy(
    ENV['TUMBLR_CONSUMER_KEY'],
    ENV['TUMBLR_CONSUMER_SECRET']
)

auth_props = t1.get_authentication_tokens(callback_url='http://localhost:8000')
auth_url = auth_props['url']

OAUTH_TOKEN_SECRET = auth_props['oauth_token_secret']

print 'Connecting with tumblr via: %s' % auth_url

# Second step

def get_query_dict(url_string):
    url, parts = urllib.splitquery(url_string)
    return dict([tuple(kv.split("=") for kv in parts.split("&"))])

request_GET = get_query_dict(auth_url)

OAUTH_TOKEN = request_GET.get('oauth_token')
oauth_verifier = request_GET.get('oauth_verifier')

t2 = tumblpy.Tumblpy(
    ENV['TUMBLR_CONSUMER_KEY'],
    ENV['TUMBLR_CONSUMER_SECRET'],
    OAUTH_TOKEN,
    OAUTH_TOKEN_SECRET
)

authorized_tokens = t2.get_authorized_tokens(oauth_verifier)

final_oauth_token = authorized_tokens['oauth_token']
final_oauth_token_secret = authorized_tokens['oauth_token_secret']




