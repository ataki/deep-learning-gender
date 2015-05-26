from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

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

def get_connection():
	global engine
	if engine is None:
		print "Engine missing!!! Aborting"
		sys.exit(1)

	return engine.connect()

### Auto-Init on Import

init("db/db.sqlite")

### Models
# for author_genders, default 0 => unclassified
# 	1 => male
# 	-1 => female

class TumblrPost(Base):
	__tablename__ = 'tumblr_oauth'

	id = Column(Integer, primary_key=True)
	post = Column(String)
	blogname = Column(String)
	post_id = Column(String)
	timestamp = Column(String)
	author_gender = Column(Integer, default=0)

class TwitterPost(Base):
	__tablename__ = 'post'

	id = Column(Integer, primary_key=True)
	post = Column(String)
	username = Column(String)
	profile_image_url = Column(String)
	timestamp = Column(String)
	author_gender = Column(Integer, default=0)

class Book(Base):
	__tablename__ = 'book'

	id = Column(Integer, primary_key=True)
	author = Column(String)
	title = Column(String)
	e_id = Column(Integer)
	century = Column(Integer)
	text_file_path = Column(String)	
	author_gender = Column(Integer, default=0)

class TaskCompletion(Base):
	__tablename__ = 'task_completion'

	id = Column(Integer, primary_key=True)
	src = Column(String)
	timestamp = Column(String)

	@classmethod
	def last_updated(type):
		conn = get_connection()
		query = text("select max(timestamp) from task_completion where type=:type")
		results = conn.execute(query, type=type).fetchall()

		try:
			first_row = results[0]
			return datetime.fromtimestamp(int(first_row[0]))
		except:
			return None

### Create all

Base.metadata.create_all(engine)