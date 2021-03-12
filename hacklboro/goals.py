import sqlite3

from hacklboro.database import DATABASE_FILE


def create_goal(user: int, percentage: float, name: str, increasing: bool):
    with sqlite3.connect(DATABASE_FILE) as con:
        con.execute(
            """
            INSERT INTO goals (user, percentage, name, increasing) VALUES (?, ?, ?, ?)
            """,
            (user, percentage, name, increasing)
        )


def update_goal(id: int, percentage: float):
    with sqlite3.connect(DATABASE_FILE) as con:
        con.execute(
            "UPDATE goals SET percentage = ? WHERE id = ?",
            (percentage, id)
        )
