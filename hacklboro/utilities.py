import sqlite3
import json


def row_to_json(row: sqlite3.Row) -> str:
    d = {}
    for key in row.keys():
        d[key] = row[key]

    return json.dumps(d)
