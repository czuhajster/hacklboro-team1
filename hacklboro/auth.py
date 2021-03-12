from flask_login import UserMixin
from passlib.hash import bcrypt
from database import DATABASE_FILE

import sqlite3


class User(UserMixin):
    @staticmethod
    def get_from_userid(userid):
        with sqlite3.connect(DATABASE_FILE) as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id=?", userid)
            return cur.fetchone()

    @staticmethod
    def get_from_username(username):
        with sqlite3.connect(DATABASE_FILE) as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE username=?", (username,))
            return cur.fetchone()

    @staticmethod
    def create(username, password):
        with sqlite3.connect(DATABASE_FILE) as con:
            password = bcrypt.hash(password)
            cur = con.cursor()
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            con.commit()

    @staticmethod
    def verify(username, password):
        user = User.get_from_username(username)
        return bcrypt.verify(password, user["password"])

    def __init__(self, userid):
        self.userid = userid

    def get_id(self):
        return str(self.userid)
