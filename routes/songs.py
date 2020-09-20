import os

from flask.helpers import url_for
from util import random_string
from flask.globals import request
from models.database import db_connection
from werkzeug.utils import redirect, secure_filename
from flask import Blueprint, abort, render_template, current_app, send_from_directory

bp = Blueprint('songs', __name__, url_prefix='/songs')

ALLOWED_EXTENSIONS = {'mp3'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Custom static data
@bp.route('/<path:filename>')
def custom_static(filename):
    return send_from_directory(current_app.config['CUSTOM_STATIC_PATH'], filename)


@bp.route('/stream', methods=['GET'])
def stream():
    song_public_id = request.args.get('id')

    query = 'SELECT title, filename, song_public_id FROM songs WHERE song_public_id=?;'
    args = (song_public_id,)

    db = db_connection()
    get = db.get(query, args, one=True)
    if get is not None:
        title = get[0]
        filename = get[1]
        id = get[2]
        return render_template('stream.html', title=title, filename=filename, id=id)

    return 'URL is invalid'


@bp.route('/view', methods=['GET'])
def view():
    query = 'SELECT title, artist, album, song_public_id FROM songs;'

    db = db_connection()
    songs_list = db.get(query)

    if len(songs_list) == 0:
        error_message = 'No Data Found'
        return render_template('error.html', error_message=error_message)

    elif songs_list is not None:
        share_url = 'http://{}:{}/songs/stream?id='.format(current_app.config['DOMAIN_NAME'],
                                                           current_app.config['PORT'])

        delete_url = 'http://{}:{}/songs/delete?id='.format(current_app.config['DOMAIN_NAME'],
                                                            current_app.config['PORT'])

        table_col = ['Title', 'Artist', 'Album', 'Share', 'Action']

        return render_template('songs.html', table_col=table_col, share_url=share_url, delete_url=delete_url, table_row=songs_list)

    else:
        return render_template('error.html', error_message=songs_list)


@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')

    elif request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        album = request.form['album']
        song_public_id = random_string()

        if 'file' not in request.files:
            error_message = 'No file is attached'
            return render_template('error.html', error_message=error_message)

        file = request.files['file']

        if file.filename == '':
            error_message = 'No selected file'
            return render_template('error.html', error_message=error_message)

        if not file and allowed_file(file.filename) is False:
            error_message = 'Allowed only .mp3 files'
            return render_template('error.html', error_message=error_message)

        filename = title + '.mp3'
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        query = 'INSERT INTO songs(song_public_id, title, artist, album, filename) values (?, ?, ?, ?, ?);'
        args = (song_public_id, title, artist, album, filename)

        db = db_connection()
        insert = db.insert(query, args)
        if insert is not True:
            error_message = 'Error while uploading the song'
            return render_template('error.html', error_message=error_message)

        file.save(file_path)
        success_message = 'File uploaded successfully'
        return render_template('success.html', success_message=success_message)

    else:
        return abort(404)


@bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')

    elif request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        album = request.form['album']

        if title != '':
            query = "SELECT title, artist, album, song_public_id FROM songs WHERE title LIKE ?;"
            args = ("%" + title + "%", )

        elif artist != '':
            query = "SELECT title, artist, album, song_public_id FROM songs WHERE artist LIKE ?;"
            args = ("%" + artist + "%", )

        elif album != '':
            query = "SELECT title, artist, album, song_public_id FROM songs WHERE album LIKE ?;"
            args = ("%" + album + "%", )

        else:
            error_message = "Invalid song search attribute"
            return render_template("error.html", error_message=error_message)

        db = db_connection()
        songs_list = db.get(query, args)

        if len(songs_list) == 0:
            error_message = 'No Data Found'
            return render_template('error.html', error_message=error_message)

        elif songs_list is not None:
            share_url = 'http://{}:{}/songs/stream?id='.format(current_app.config['DOMAIN_NAME'],
                                                               current_app.config['PORT'])

            delete_url = 'http://{}:{}/songs/delete?id='.format(current_app.config['DOMAIN_NAME'],
                                                                current_app.config['PORT'])

            table_col = ['Title', 'Artist', 'Album', 'Share', 'Action']

            return render_template('search.html', table_col=table_col, share_url=share_url, delete_url=delete_url, table_row=songs_list)

        else:
            error_message = 'No Data Found'
            return render_template('error.html', error_message=error_message)

    else:
        abort(404)


@bp.route('/delete', methods=['GET'])
def delete():
    song_public_id = request.args.get('id')

    query = 'DELETE FROM songs WHERE song_public_id=?;'
    args = (song_public_id,)

    db = db_connection()
    delete = db.delete(query, args)
    if delete is True:
        success_message = 'Song deleted successfully'
        return render_template('success.html', success_message=success_message)

    else:
        error_message = delete
        return render_template('error.html', error_message=error_message)


@bp.route('/download', methods=['GET'])
def download():
    song_public_id = request.args.get('id')

    query = 'SELECT filename FROM songs WHERE song_public_id=?;'
    args = (song_public_id,)

    db = db_connection()
    get = db.get(query, args, one=True)

    if len(get) == 0:
        error_message = 'No Data Found'
        return render_template('error.html', error_message=error_message)

    elif get is not None:
        filename = get[0]
    
    else:
        return render_template('error.html', error_message=get)

    directory = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=directory, filename=filename, as_attachment=True)
