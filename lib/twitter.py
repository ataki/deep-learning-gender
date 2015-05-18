import twitter
import sys
import os

ENV = os.environ

class Client(boj):
	def __init__(self):
		self.client = twitter.Api(
		    consumer_key=ENV['TWITTER_CONSUMER_KEY'],
		    consumer_secret=ENV['TWITTER_CONSUMER_SECRET'],
		    access_token_key=ENV['TWITTER_ACCESS_TOKEN'],
		    access_token_secret=ENV['TWITTER_ACCESS_TOKEN']
		)

		if self.client.VerifyCredentials():
		    print "Twitter verification failed"
		    sys.exit(1)

	def get_posts(self, since="2010-01-01"):
		terms = ['fashion', 'action', 'movies', 'apple', 
			'stock', 'obama', 'campaign', 'warcraft', 
			'starcraft', 'loreal', 'diy']		

		accum = []
		for term in terms:
			results = self.client.GetSearch(
				term=term,
				since=since,
				count=100,
				include_entities=True,
				locale='ja'
			)
			accum.append(map(self.to_sql_row, results))
		return accum

	def to_sql_row(self, row):
		post = result['text']
		username = result['user']['name']
		profile_image_url = result['user']['profile_image_url']
		timestamp = result['created_at']
		return {
			'post': post, 
			'username': username, 
			'profile_image_url': profile_image_url, 
			'timestamp': timestamp
		}	