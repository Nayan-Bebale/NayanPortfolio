# main.py
import os
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_session import Session
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from config import Config
from models import db, Project, Achievement
from forms import ProjectForm, AchievementForm

mail = Mail()
app = Flask(__name__)
app.config.from_object(Config)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

db.init_app(app)
mail.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    achievements = Achievement.query.all()

    web_projects = Project.query.filter(Project.category.contains('web')).all()
    app_projects = Project.query.filter(Project.category.contains('app')).all()
    other_projects = Project.query.filter(Project.category.contains('other')).all()

    return render_template('index.html', web_projects=web_projects,
                           app_projects=app_projects, other_projects=other_projects, achievements=achievements)


@app.route('/details/<project>')
def details(project):
    project = Project.query.get_or_404(project)
    return render_template('portfolio-details.html', project=project)


@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message_body = request.form['message']

        msg = Message(subject,
                      sender=email,
                      recipients=[app.config['MAIL_USERNAME']],
                      body=f"Name: {name}\nEmail: {email}\n\n{message_body}")

        try:
            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            flash(f'Failed to send message. Error: {str(e)}', 'danger')

    return redirect('/')


@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if not session.get('admin'):
        flash('You are not authorized to perform this action.', 'danger')
        return redirect(url_for('index'))
    form = ProjectForm()
    if form.validate_on_submit():
        image1_filename = secure_filename(form.image1.data.filename)
        form.image1.data.save(os.path.join(app.config['UPLOADED_IMAGES_DEST'], image1_filename))

        image2_filename = secure_filename(form.image2.data.filename) if form.image2.data else None
        if image2_filename:
            form.image2.data.save(os.path.join(app.config['UPLOADED_IMAGES_DEST'], image2_filename))

        image3_filename = secure_filename(form.image3.data.filename) if form.image3.data else None
        if image3_filename:
            form.image3.data.save(os.path.join(app.config['UPLOADED_IMAGES_DEST'], image3_filename))

        project = Project(
            name=form.name.data,
            website_link=form.website_link.data,
            image1=image1_filename,
            image2=image2_filename,
            image3=image3_filename,
            description=form.description.data,
            github_link=form.github_link.data,
            category=','.join(form.category.data)
        )
        db.session.add(project)
        db.session.commit()
        flash('Project has been added!', 'success')
        return redirect(url_for('add_project'))
    return render_template('add_project.html', form=form)


@app.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    if not session.get('admin'):
        flash('You are not authorized to perform this action.', 'danger')
        return redirect(url_for('index'))

    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/add_achievement', methods=['GET', 'POST'])
def add_achievement():
    if not session.get('admin'):
        flash('You are not authorized to perform this action.', 'danger')
        return redirect(url_for('index'))
    form = AchievementForm()
    if form.validate_on_submit():
        image_filename = secure_filename(form.image.data.filename) if form.image.data else None
        if image_filename:
            form.image.data.save(os.path.join(app.config['UPLOADED_IMAGES_DEST'], image_filename))

        achievement = Achievement(
            name=form.name.data,
            organization=form.organization.data,
            date=form.date.data,
            description=form.description.data,
            image=image_filename
        )
        db.session.add(achievement)
        db.session.commit()
        flash('Achievement has been added!', 'success')
        return redirect(url_for('add_achievement'))
    return render_template('add_achievement.html', form=form)


@app.route('/achievement_detail/<int:achievement>')
def achievement_detail(achievement):
    achievement = Achievement.query.get_or_404(achievement)
    return render_template('activement-detail.html', data=achievement)


@app.route('/delete_achievement/<int:achievement_id>', methods=['POST'])
def delete_achievement(achievement_id):
    if not session.get('admin'):
        flash('You are not authorized to perform this action.', 'danger')
        return redirect(url_for('index'))

    achievement = Achievement.query.get_or_404(achievement_id)
    db.session.delete(achievement)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=False)
