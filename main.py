# coding: utf-8

from flask import Flask

DEBUG = True

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello world'

if __name__ == '__main__':
    app.run('0.0.0.0', 8000, debug=DEBUG)