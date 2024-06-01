import os
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_session import Session
from flask_mail import Mail, Message
from flask_uploads import configure_uploads, IMAGES, UploadSet
from config import Config
from models import db, Project

mail = Mail()
images = UploadSet('images', IMAGES)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SESSION_TYPE'] = 'filesystem'  # Using the filesystem for simplicity
    Session(app)

    db.init_app(app)
    mail.init_app(app)
    configure_uploads(app, images)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        web_projects = Project.query.filter(Project.category.contains('web')).all()
        app_projects = Project.query.filter(Project.category.contains('app')).all()
        other_projects = Project.query.filter(Project.category.contains('other')).all()

        return render_template('index.html', web_projects=web_projects,
                               app_projects=app_projects, other_projects=other_projects)

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
        from forms import ProjectForm
        form = ProjectForm()
        if form.validate_on_submit():
            image1_filename = images.save(form.image1.data)
            image2_filename = images.save(form.image2.data) if form.image2.data else None
            image3_filename = images.save(form.image3.data) if form.image3.data else None

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

        # Retrieve the project from the database
        project = Project.query.get_or_404(project_id)

        # Delete the project from the database
        db.session.delete(project)
        db.session.commit()

        # Redirect to the home page or any other relevant page
        return redirect(url_for('index'))

    @app.route('/check')
    def check():
        return render_template('inner-page.html')

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="localhost", port=5000)
