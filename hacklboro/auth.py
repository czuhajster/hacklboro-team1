from flask_login import UserMixin
from passlib.hash import bcrypt

from hacklboro.database import DATABASE_FILE

import sqlite3


class User(UserMixin):
    @staticmethod
    def get_from_userid(userid):
        """
        Gets the user's data in a sqlite3.Row format from the given ID
        """
        with sqlite3.connect(DATABASE_FILE) as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id=?", (userid,))
            return cur.fetchone()

    @staticmethod
    def get_from_username(username: str):
        """
        Gets the user's data in a sqlite3.Row format from the given username
        Note that case sensitivity doesn't matter for this method
        """
        username = username.lower()
        with sqlite3.connect(DATABASE_FILE) as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE LOWER(username)=?", (username,))
            return cur.fetchone()

    @staticmethod
    def create(username, password):
        """
        Creates a new user with the given username and password
        Note that the password is hashed before being inserted into the database
        """
        with sqlite3.connect(DATABASE_FILE) as con:
            password = bcrypt.hash(password)
            cur = con.cursor()
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            con.commit()

    @staticmethod
    def verify(username, password):
        """
        Verifies that the password from the user is the same as the password that was given to the method
        """
        user = User.get_from_username(username)
        if user:
            return bcrypt.verify(password, user["password"])
        return False

    def __init__(self, userid):
        """
        Constructor for the user
        """
        self.userid = userid
        self.username = User.get_from_userid(userid)["username"]

    def get_id(self):
        """
        Getter for the user ID
        """
        return str(self.userid)
