from itsdangerous import URLSafeTimedSerializer
from project import app, mail
from flask_mail import Message
from flask import render_template, current_app
from threading import Thread

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=86400):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    email = serializer.loads(
        token,
        salt=app.config['SECURITY_PASSWORD_SALT'],
        max_age=expiration)
    return email

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_token(subject, html, name, email, confirm_url):
    app = current_app._get_current_object()
    msg = Message(subject, sender="noreply.slowcrm@gmail.com", recipients=[email])
    msg.html = render_template(html, name = name, confirm_url = confirm_url)
    thr = Thread(target=send_async_email, args=[app,msg])
    thr.start()
    return thr
