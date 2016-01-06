from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    return request.form

@app.route('/<target>')
def redirect(target):
    pass

if __name__ == '__main__':
    app.run()