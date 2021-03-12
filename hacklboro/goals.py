import sqlite3

from sqlite3 import Cursor

from hacklboro.database import DATABASE_FILE
from hacklboro.utilities import row_list_to_json


def create_goal(user: int, percentage: float, name: str, increasing: bool) -> None:
    with sqlite3.connect(DATABASE_FILE) as con:
        con.execute(
            """
            INSERT INTO goals (user, percentage, name, increasing) VALUES (?, ?, ?, ?)
            """,
            (user, percentage, name, increasing)
        )


def update_goal(id: int, user: int, percentage: float) -> bool:
    with sqlite3.connect(DATABASE_FILE) as con:
        # Perform check to make sure the goal belongs to the user before updating it
        cur: Cursor = con.execute("SELECT user FROM goals WHERE id = ?", (id, ))
        result = cur.fetchone()[0]

        if result == user:
            con.execute(
                "UPDATE goals SET percentage = ? WHERE id = ?",
                (percentage, id)
            )
            return True

        return False


def get_goals(user: int, limit: int = 20) -> list[sqlite3.Row]:
    with sqlite3.connect(DATABASE_FILE) as con:
        con.row_factory = sqlite3.Row
        cur: Cursor = con.execute(
            "SELECT * FROM goals WHERE user = ? ORDER BY id DESC LIMIT ?",
            (user, limit)
        )
        return cur.fetchall()


def get_goals_as_json(user: int, limit: int = 20) -> str:
    rows = get_goals(user, limit)
    return row_list_to_json(rows)
