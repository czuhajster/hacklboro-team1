import sqlite3

from sqlite3 import Cursor

from hacklboro.database import DATABASE_FILE


def get_companies() -> list[sqlite3.Row]:
    with sqlite3.connect(DATABASE_FILE) as con:
        con.row_factory = sqlite3.Row
        cur: Cursor = con.execute("SELECT * FROM company")
        return cur.fetchall()
