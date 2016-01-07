import sys

import short_url
import Helper
import Config

from urllib.parse import urlparse
from datetime import datetime

from flask import Flask
from flask import request, jsonify, render_template, redirect

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.config['db_connection_string']

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

    def __init__(self, ip):
        self.ip = ip
        self.visit_time = datetime.now()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
@Helper.jsonp
def add():

    if request.form['url'].strip() == "":
        return jsonify({'message': 'Url is empty'})
    elif urlparse(request.form['url']).netloc.strip() == '':
        return jsonify({'message': 'Url is illegal'})

    key = short_url.encode_url(len(Map.query.all()))
    url = request.form['url']

    exists_query = Map.query.filter_by(url = url).first()
    
    if exists_query != None:
        key = exists_query.key
    else:
        db.session.add(Map(key, url))

    db.session.add(Visit(request.environ['REMOTE_ADDR']))
    db.session.commit()

    return jsonify({'url': request.url_root + key})

@app.route('/<key>', methods=['GET'])
def go(key):
    result = Map.query.get(key)
    if result == None:
        return jsonify({'message': 'Not Found'})
    else:
        return redirect(result.url)

if __name__ == '__main__':
    if sys.argv[1] == 'init':
        db.create_all()
    elif sys.argv[1] == 'run':
        app.run(debug = True)
