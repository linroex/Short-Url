from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add')
def add():
    pass

@app.route('/<target>')
def redirect(target):
    pass

if __name__ == '__main__':
    app.run()