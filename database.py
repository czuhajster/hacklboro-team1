''' Create database.'''

import sqlite3

con = sqlite3.connect('database.db')
cur = con.cursor()

cur.execute('''CREATE TABLE goals (id integer primary key, user integer,
            percentage real, name text, increasing integer);''')
cur.execute('''CREATE TABLE user (id integer primary key, username varchar(255),
            password varchar(255));''')
