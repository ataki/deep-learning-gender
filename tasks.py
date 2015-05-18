"""
Scheduled tasks for retrieving datasets given limit
"""

from lib import tumblr
from lib import twitter
from lib.model import TwitterPost, TumblrPost, TaskCompletion
from lib.model import get_session

from sqlalchemy.sql import func as F

import schedule

def fetch_twitter():
	client = twitter.Client()
	last_updated = TaskCompletion.last_updated("twitter")

	if last_updated is None:
		posts = client.get_posts()
	else:
		posts = client.get_posts(since=datetime.strftime(last_updated, "%Y-%m-%d"))

	session = get_session()
	for json in posts:
		inst = TwitterPost(**json)
		session.add(inst)
	session.commit()
