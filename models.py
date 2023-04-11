from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class URL(db.Model):
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
        db.Text,
        nullable=False
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

    listings = db.relationship('Listings', backref="URL")


class Listing(db.Model):
    """Listings from Craigslist queries"""

    __tablename__ = 'listings'

    id = db.Column(
        db.Integer,
        nullable=False,
        unique=True
    )

    url = db.Column(
        db.String,
        nullable=False,
        unique=True
    )

    title = db.Column(
        db.String,
        nullable=False
    )

    img_url = db.Column (
        db.String,
        nullable=False
    )

    price = db.Column(
        db.Integer,
        nullable=True
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )


