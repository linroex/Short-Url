import sys

import short_url
import Helper

from urllib.parse import urlparse
from datetime import datetime

from Config import config

from flask import Flask
from flask import request, jsonify, render_template, redirect

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
app.config['SQLALCHEMY_DATABASE_URI'] = config['db_connection_string']

db = SQLAlchemy(app)

class Map(db.Model):
    key = db.Column(db.String(10), primary_key=True)
    url = db.Column(db.Text())
    created = db.Column(db.DateTime())

    def __init__(self, key, url):
        self.key = key
        self.url = url
        self.created = datetime.now()

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(15))
    visit_time = db.Column(db.DateTime())
    action = db.Column(db.Enum('add', 'go'))

    def __init__(self, ip, action):
        self.ip = ip
        self.action = action
        self.visit_time = datetime.now()

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

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
@Helper.jsonp
def add():

    # URL Validate
    if request.form['url'].strip() == "":
        return jsonify({'message': 'Url is empty'})
    elif urlparse(request.form['url']).netloc.strip() == '':
        return jsonify({'message': 'Url is illegal'})

    # Usage check
    user_today_usage = len(Visit.query.filter(Visit.action == 'add', Visit.ip == request.environ['REMOTE_ADDR'], Visit.visit_time >= datetime.now().date()).all())
    
    if user_today_usage > config['add_quota_per']:
        return jsonify({'message': 'Today usage is exceed'})

    key = short_url.encode_url(len(Map.query.all()) + config['offset'])
    url = request.form['url']

    exists_query = Map.query.filter_by(url = url).first()
    
    if exists_query != None:
        # If url is exists
        key = exists_query.key
    else:
        db.session.add(Map(key, url))

    db.session.add(Visit(request.environ['REMOTE_ADDR'], 'add'))
    db.session.commit()

    return jsonify({'url': config['domain'] + key})

@app.route('/<key>', methods=['GET'])
def go(key):
    result = Map.query.get(key)
    if result == None:
        return jsonify({'message': 'Not Found'})
    else:
        db.session.add(Visit(request.environ['REMOTE_ADDR'], 'go'))
        db.session.commit()

        return redirect(result.url)

if __name__ == '__main__':
    if sys.argv[1] == 'init':
        db.drop_all()
        db.create_all()
    elif sys.argv[1] == 'run':
        app.run(debug = True)
    elif sys.argv[1] == 'migrate':
        db.create_all()
