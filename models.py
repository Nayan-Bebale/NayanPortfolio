# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    website_link = db.Column(db.String(200))
    image1 = db.Column(db.String(200))
    image2 = db.Column(db.String(200))
    image3 = db.Column(db.String(200))
    description = db.Column(db.Text)
    github_link = db.Column(db.String(200))
    category = db.Column(db.String(120))

    def __repr__(self):
        return f'<Project {self.name}>'


class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    organization = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Achievement {self.name}>'
