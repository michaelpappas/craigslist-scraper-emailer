from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class URLs(db.Model):
    """Search URLs to find listings."""

    __tablename__= 'urls'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    url = db.Column(
        db.text,
        nullable=False
    )

    listings = db.relationship('Listings', backref="URL")


class Listings(db.Model):
    """Listings from Craigslist queries"""

    __tablename__ = 'listings'

    id = db.Column(
        db.integer,
        nullable=False,
        unique=True
    )

