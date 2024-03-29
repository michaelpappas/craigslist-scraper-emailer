import os
from dotenv import load_dotenv

from flask import Flask, render_template,flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import URLAddForm
from models import db, connect_db, URL

load_dotenv()

scraper_enable = True

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route('/', methods=["GET","POST"])
def homepage():
    """Renders homepage
    Allows user to view search queries and toggle active/inactive
    Renders form for adding search queries."""
    searches = URL.query.all()
    form = URLAddForm()
    if form.validate_on_submit():
        try:
            url = URL.add_search(
                name = form.name.data,
                search_url = form.search_url.data
            )
            db.session.commit()
        except IntegrityError:
            flash("That url is already in use", "danger")
            return render_template('home.html', form=form)

        flash("New Search Successfully Added!", 'success')
        return redirect("/")


    else:
        return render_template('home.html', form=form, searches=searches)


@app.post('/searches/<int:search_id>/activate/')
def activate_search(search_id):
    """Change URL active status to true"""
    search = URL.query.get_or_404(search_id)
    search.active = True
    db.session.commit()

    return redirect('/')

@app.post('/searches/<int:search_id>/deactivate')
def deactivate_search(search_id):
    """Change URL active status to false"""
    search = URL.query.get_or_404(search_id)
    search.active = False
    db.session.commit()

    return redirect('/')
@app.post('/searches/<int:search_id>/delete')
def delete_search(search_id):
    """Delete search from db"""
    search = URL.query.get_or_404(search_id)
    db.session.delete(search)
    db.session.commit()

    return redirect('/')

@app.post('/enable')
def enable_scraper():
    """Change scraper_enable to True"""
    scraper_enable = True

    return redirect('/')

@app.post('/disable')
def disable_scraper():
    """Change scraper_enable to False"""
    scraper_enable = False

    return redirect('/')