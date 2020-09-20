# import sqlite3


# class SqliteDB:
#     def connect(self, db_file):
#         self.conn = sqlite3.connect(db_file)

#     def get_all(self, query):
#         cur = self.conn.execute(query)
#         rv = cur.fetchall()
#         self.close()
#         return rv

#     def insert(self, query):
#         pass

#     def delete(self, query):
#         pass

#     def update(self, query):
#         pass

#     def close(self):
#         self.conn.close()


# def db_connection():
#     db = SqliteDB()
#     if db.connect("songs.db") is False:
#         return False

#     return db


import sqlite3
from flask import g, current_app


def get_db():
    conn = getattr(g, '_database', None)
    if conn is None:
        conn = g._database = sqlite3.connect(current_app.config['DATABASE'])
        conn.row_factory = lambda cursor, row: list(row)
    return conn


class Database:
    def __init__(self) -> None:
        self.conn = get_db()

    def insert(self, query, args):
        try:
            cur = self.conn.cursor()
            cur.execute(query, args)
            self.conn.commit()
            return True

        except Exception as e:
            return e

    def get(self, query, args=(), one=False):
        try:
            cur = self.conn.cursor()
            cur.execute(query, args)
            self.conn.commit()

            if one is True:
                return cur.fetchone()

            return cur.fetchall()

        except Exception as e:
            return e

    def delete(self, query, args):
        try:
            cur = self.conn.cursor()
            cur.execute(query, args)
            self.conn.commit()
            return True

        except Exception as e:
            return e


def db_connection():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._conn = Database()

    return db
