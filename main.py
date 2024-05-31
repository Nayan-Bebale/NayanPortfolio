import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from data import data

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("secret_key")

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

# Configurations for Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('main_mail')
app.config['MAIL_PASSWORD'] = os.environ.get('mail_password')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('main_mail')

db = SQLAlchemy(app)
mail = Mail(app)


@app.route('/')
def index():
    return render_template('index.html', data=data)


@app.route('/details/<project>')
def details(project):
    project = data[project]
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


@app.route('/check')
def check():
    return render_template('inner-page.html')


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, host="localhost", port=5000)
