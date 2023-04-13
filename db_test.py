from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import db, URL, Listing

import os
from dotenv import load_dotenv

load_dotenv()
db_string = os.environ['DATABASE_URL']

db = create_engine(db_string)

Session = sessionmaker(db)
session = Session()


listings = session.query(Listing)

