# fetch_data.py
from models import db, Project, Achievement
from flask import Flask
from config import Config
import json

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

projects_dict = []
achievements_dict = []

with app.app_context():
    projects = Project.query.all()
    for project in projects:
        project_data = {
            'id': project.id,
            'name': project.name,
            'website_link': project.website_link,
            'image1': project.image1,
            'image2': project.image2,
            'image3': project.image3,
            'description': project.description,
            'github_link': project.github_link,
            'category': project.category
        }
        projects_dict.append(project_data)

    achievements = Achievement.query.all()
    for achievement in achievements:
        achievement_data = {
            'id': achievement.id,
            'name': achievement.name,
            'organization': achievement.organization,
            'date': str(achievement.date),
            'description': achievement.description,
            'image': achievement.image
        }
        achievements_dict.append(achievement_data)

# Save the data to data.py
with open('data.py', 'w', encoding='utf-8') as f:
    f.write("projects = " + json.dumps(projects_dict, ensure_ascii=False, indent=4) + "\n")
    f.write("achievements = " + json.dumps(achievements_dict, ensure_ascii=False, indent=4) + "\n")

print("Data fetched and stored in data.py")
