from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

import sys

engine = None
session = None
Base = declarative_base()

def init(dbpath):
	global engine
	engine = create_engine('sqlite:///' + dbpath, echo=True)

def get_session():
	global session, engine
	if engine is None:
		print "Engine missing!!! Aborting"
		sys.exit(1)

	if session is None:
		S = sessionmaker(bind=engine)
		session = S()

	return session

### Auto-Init on Import

init("db/db.sqlite")

### Models

class TumblrPost(Base):
	__tablename__ = 'tumblr_oauth'

	id = Column(Integer, primary_key=True)
	post = Column(String)
	blogname = Column(String)
	post_id = Column(String)
	timestamp = Column(String)
	# Male => 1, Female => -1
	author_gender = Column(Integer, default=0)

class TwitterPost(Base):
	__tablename__ = 'post'

	id = Column(Integer, primary_key=True)
	post = Column(String)
	username = Column(String)
	profile_image_url = Column(String)
	timestamp = Column(String)
	# Male => 1, Female => -1
	author_gender = Column(Integer, default=0)

### Create all

Base.metadata.create_all(engine)