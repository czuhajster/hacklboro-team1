import sqlite3
from sqlite3 import Cursor
from typing import List

from hacklboro.database import DATABASE_FILE


def get_companies() -> List[sqlite3.Row]:
    """
    Get all the companies with their info for the traffic light page
    """
    with sqlite3.connect(DATABASE_FILE) as con:
        con.row_factory = sqlite3.Row
        cur: Cursor = con.execute("SELECT * FROM company")
        return cur.fetchall()
