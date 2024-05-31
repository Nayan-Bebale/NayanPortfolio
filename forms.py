from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, URLField, SubmitField
from wtforms.validators import DataRequired, URL


class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    website_link = URLField('Website Link', validators=[URL()])
    image1 = URLField('Image 1 URL', validators=[URL()])
    image2 = URLField('Image 2 URL', validators=[URL()])
    image3 = URLField('Image 3 URL', validators=[URL()])
    description = TextAreaField('Description', validators=[DataRequired()])
    github_link = URLField('GitHub Link', validators=[URL()])
    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Add Project')