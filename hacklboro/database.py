import os
import sqlite3
from sqlite3 import Connection

DATABASE_FILE = "hacklboro/database.db"
SCHEMA_FILE = "hacklboro/sqlite_schema"


def init_db():
    with open(SCHEMA_FILE) as f:
        text = f.read()
        con.executescript(text)
        con.commit()


if not os.path.isfile(DATABASE_FILE):
    con = sqlite3.connect(DATABASE_FILE)
    init_db()
    con.close()

con: Connection = sqlite3.connect(DATABASE_FILE)
