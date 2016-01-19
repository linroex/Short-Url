import csv
import requests

from requests.auth import HTTPBasicAuth
from Config import config

from flask import Flask

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
app.config['SQLALCHEMY_DATABASE_URI'] = config['db_connection_string']

db = SQLAlchemy(app)

class Email_Apply(db.Model):
    token = db.Column(db.String(65), primary_key=True)
    realname = db.Column(db.String(15))
    username = db.Column(db.String(15))
    email = db.Column(db.String(255))

    def __init__(self, realname, username, email, token):
        self.token = token
        self.realname = realname
        self.username = username
        self.email = email

def generate_verify_token(email):
    import hashlib
    from time import time

    return hashlib.sha224((email + str(time()) + config['secret']).encode('utf8')).hexdigest()

def get_random_password(length):
    from random import choice
    from string import ascii_uppercase

    return ''.join([choice(ascii_uppercase) for c in range(length)])

def add_smtp_credentials(login, password):
    return requests.post(
        '{API_URL}/domains/{DOMAIN}/credentials'.format(API_URL=config['API_URL'], DOMAIN=config['DOMAIN']), 
        auth = HTTPBasicAuth('api', config['API_KEY']), 
        data = {
            'login': login,
            'password': password
        }
    )

def send_mail(receiver, template, data):
    subject = 'NTUST.ME 電子信箱申請確認信'
    content = open('templates/' + template, encoding='utf-8').read().format(**data)

    return requests.post(
        '{API_URL}/{DOMAIN}/messages'.format(API_URL=config['API_URL'], DOMAIN=config['DOMAIN']),
        auth=("api", config['API_KEY']),
        data={"from": config['SENDER'],
            "to": receiver,
            "subject": subject,
            "html": content,
            "o:tracking-opens":True})

def add_forward_route(login, forward_dest):
    return requests.post(
        '{API_URL}/routes'.format(API_URL=config['API_URL']),
        auth = HTTPBasicAuth('api', config['API_KEY']), 
        data = {
            'priority': 0,
            'description': '{login}@{DOMAIN} forward route'.format(login=login, DOMAIN=config['DOMAIN']),
            "expression": 'match_recipient("{login}@{DOMAIN}")'.format(login=login, DOMAIN=config['DOMAIN']),
            "action": 'forward("{dest}")'.format(dest=forward_dest)
        }
    )

def main():
    with open('/Users/linroex/Downloads/NTUST.ME 信箱封測申請-report.csv', encoding='utf8') as f:
        f.readline()
        appliers = csv.reader(f)

        for applier in appliers:
            name = applier[1]
            login = applier[2]
            email = applier[3]
            token = generate_verify_token(email)
            
            send_mail(email, 'verify_mail.html', data = {'name': name, 'token': token})

            db.session.add(Email_Apply(name, login, email, token))
            db.session.commit()
            exit()

if __name__ == '__main__':
    main()