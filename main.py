import sys

from flask import Flask
from flask import request, jsonify, render_template, redirect

from flask_sqlalchemy import SQLAlchemy

import short_url

app = Flask(__name__)

app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)

class Map(db.Model):
    key = db.Column(db.String(10), primary_key=True)
    url = db.Column(db.Text())

    def __init__(self, key, url):
        self.key = key
        self.url = url

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    key = short_url.encode_url(len(Map.query.all()))
    url = request.form['url']

    db.session.add(Map(key, url))
    db.session.commit()

    return jsonify({'url': request.url_root + key})

@app.route('/<key>')
def go(key):
    result = Map.query.get(key)
    if result == None:
        return jsonify({'code': 'Not Found'})
    else:
        return redirect(Map.query.get(key).url)

if __name__ == '__main__':
    if sys.argv[1] == 'init':
        db.create_all()
    elif sys.argv[1] == 'run':
        app.run()
    elif sys.argv[1] == 'test':
        pass