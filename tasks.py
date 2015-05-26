"""
Defines tasks to be scheduled for retrieving datasets given limit
"""

from lib import tumblr
from lib import twitter
from lib.model import TwitterPost, TumblrPost, TaskCompletion
from lib.model import get_session

from sqlalchemy.sql import func as F

def fetch_twitter():
	client = twitter.Client()
	last_updated = TaskCompletion.last_updated("twitter")

	if last_updated is None:
		posts = client.get_posts()
	else:
		since_str = datetime.strftime(last_updated, "%Y-%m-%d")
		posts = client.get_posts(since=since_str)

	session = get_session()
	for json in posts:
		inst = TwitterPost(**json)
		session.add(inst)
	session.commit()

# Mapping of tasks => run every (X, unit_of_time)
EXPORTED_TASKS = [
	(fetch_twitter, '15', 'min')
]