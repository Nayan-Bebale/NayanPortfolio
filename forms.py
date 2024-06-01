# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField, SelectMultipleField
from wtforms.validators import DataRequired, URL, Optional
from flask_wtf.file import FileAllowed, FileRequired


class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    website_link = StringField('Website Link', validators=[Optional(), URL()])
    image1 = FileField('Image 1', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    image2 = FileField('Image 2', validators=[Optional(), FileAllowed(['jpg', 'png'], 'Images only!')])
    image3 = FileField('Image 3', validators=[Optional(), FileAllowed(['jpg', 'png'], 'Images only!')])
    description = TextAreaField('Description', validators=[DataRequired()])
    github_link = StringField('GitHub Link', validators=[Optional(), URL()])
    category = SelectMultipleField('Category', choices=[
        ('web', 'Website'),
        ('app', 'Application'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    submit = SubmitField('Add Project')



class AchievementForm(FlaskForm):
    name = StringField('Certificate Name', validators=[DataRequired()])
    organization = StringField('Issuing Organization', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    description = TextAreaField('Description')
    image = FileField('Certificate Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Add Achievement')