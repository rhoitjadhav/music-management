from flask.helpers import url_for
from werkzeug.utils import redirect
from routes import songs
from flask import Flask, redirect

app = Flask(__name__)
app.config.from_json("config/config.json")

if __name__ == '__main__':
    host = app.config['HOST']
    port = app.config['PORT']
    debug = app.config['DEBUG']

    app.run(host, port, debug)
