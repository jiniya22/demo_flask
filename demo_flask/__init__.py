from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def index():
    args = {'title': 'index Page', 'contents': 'hello world'}
    return render_template('index.html', **args)
    # return render_template('index.html', title='index Page', contents='hello world')
