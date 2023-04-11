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

    search_url = db.Column(
        db.Text,
        nullable=False
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

    @classmethod
    def add_search(cls, name, search_url):
        """creates new record in URL tabel with name and search URL"""

        url = URL(
            name=name,
            search_url=search_url
        )
        db.session.add(url)
        return url


class Listing(db.Model):
    """Listings from Craigslist queries"""

    __tablename__ = 'listings'

    id = db.Column(
        db.Integer,
        primary_key=True
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



def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)


