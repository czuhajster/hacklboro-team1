import sqlite3
import json
from typing import List


def row_to_json(row: sqlite3.Row) -> str:
    """
    Converts a sqlite3.Row to a string representing JSON
    """
    d = {}
    for key in row.keys():
        d[key] = row[key]

    return json.dumps(d)


def row_list_to_json(rows: List[sqlite3.Row]) -> str:
    """
    Converts a List[sqlite3.Row] to a string representing JSON
    """
    l = []
    for row in rows:
        l.append(row_to_json(row))

    return json.dumps(l)
