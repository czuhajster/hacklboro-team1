import sqlite3
import json


def row_to_json(row: sqlite3.Row) -> str:
    d = {}
    for key in row.keys():
        d[key] = row[key]

    return json.dumps(d)


def row_list_to_json(rows: list[sqlite3.Row]) -> str:
    l = []
    for row in rows:
        l.append(row_to_json(row))

    return json.dumps(l)
