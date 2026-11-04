import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from platformdirs import user_data_path


@contextmanager
def transaction() -> Iterator[sqlite3.Connection]:
    conn = get_connection()
    try:
        with conn:
            yield conn
    finally:
        conn.close()


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(get_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def get_path() -> Path:
    path = user_data_path("rejected")
    path.mkdir(parents=True, exist_ok=True)
    return path / "rejected.sqlite"