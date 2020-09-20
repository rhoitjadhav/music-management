from flask.helpers import url_for
from werkzeug.utils import redirect
from routes import songs
from flask import Flask, redirect, render_template

app = Flask(__name__)
app.config.from_json("config/config.json")


@app.route("/")
def index():
    return redirect(url_for('songs.view'))


# Blueprints
app.register_blueprint(songs.bp)


if __name__ == '__main__':
    host = app.config['HOST']
    port = app.config['PORT']
    debug = app.config['DEBUG']

    app.run(host, port, debug)
