import os
import sqlite3

DATABASE_FILE = "hacklboro/database.db"
SCHEMA_FILE = "hacklboro/sqlite_schema"


def init_db():
    """
    Initialises the database with the script pointed to by SCHEMA_FILE
    """
    with open(SCHEMA_FILE) as f:
        text = f.read()
        con.executescript(text)
        con.commit()


# Initialise the database if the db file doesn't exist
if not os.path.isfile(DATABASE_FILE):
    con = sqlite3.connect(DATABASE_FILE)
    init_db()
    con.close()


def generate_data():
    """
    Add fake test data to the database
    Note that all tables get generated data added to them
    """

    import random
    from hacklboro.auth import User
    from hacklboro.goals import create_goal

    with sqlite3.connect(DATABASE_FILE) as con:
        for i in range(10):
            con.execute(
                """
                INSERT INTO company (name, rating, text) VALUES (?, ?, ?)
                """,
                (
                    f"Company {i}", random.randrange(0, 100),
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                    "Vestibulum et nibh erat. Cras at nulla metus."
                )
            )

    for i in range(10):
        User.create(f"User{i}", "password")

    for i in range(10):
        create_goal(i, random.random() * 100, f"Name {i}_1", random.random() > 0.5)
        create_goal(i, random.random() * 100, f"Name {i}_2", random.random() > 0.5)
        create_goal(i, random.random() * 100, f"Name {i}_3", random.random() > 0.5)
