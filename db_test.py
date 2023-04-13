from sqlalchemy import create_engine, insert
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

active_urls = session.query(URL).filter(URL.active==True).all()

print(active_urls)
listing_url = "https://sfbay.craigslist.org/sby/ctd/d/sunnyvale-373-mo-toyota-camry-le/7609987254.html"
listing = session.query(Listing).filter(Listing.url==listing_url).all()
breakpoint()
print(listing)

