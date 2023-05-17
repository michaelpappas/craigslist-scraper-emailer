from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired


class URLAddForm(FlaskForm):
    """Form for adding/editing search URLs"""

    name = TextAreaField('Name', validators=[DataRequired()])
    search_url = TextAreaField('Search URL', validators=[DataRequired()])
