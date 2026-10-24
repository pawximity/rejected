import sqlite3


def sqlite_connection(sqlite_file: str) -> sqlite3.Connection:
    conn = sqlite3.connect(sqlite_file)
    return conn