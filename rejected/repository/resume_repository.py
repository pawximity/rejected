import sqlite3

FIND_RESUME_SQL = """
    SELECT *
    FROM resumes
    WHERE id = ?
"""

FIND_ALL_RESUMES_SQL = """
    SELECT *
    FROM resumes
    ORDER BY name ASC, version DESC
"""

INSERT_RESUME_SQL = """
    INSERT INTO resumes (
        type_id, version, name
    )
    VALUES (?, ?, ?)
    RETURNING *
"""

UPDATE_RESUME_SQL = """
    UPDATE resumes
    SET type_id = ?,
        version = ?,
        name = ?,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = ?
    RETURNING *
"""

DELETE_RESUME_SQL = """
    DELETE FROM resumes
    WHERE id = ?
"""


def find(conn: sqlite3.Connection, resume_id: int) -> sqlite3.Row:
    return conn.execute(FIND_RESUME_SQL, (resume_id,)).fetchone()


def find_all(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute(FIND_ALL_RESUMES_SQL).fetchall()


def insert(
    conn: sqlite3.Connection,
    type_id: int,
    version: int,
    name: str,
) -> sqlite3.Row:
    return conn.execute(INSERT_RESUME_SQL, (type_id, version, name)).fetchone()


def update(
    conn: sqlite3.Connection,
    type_id: int,
    version: int,
    name: str,
    resume_id: int,
) -> sqlite3.Row:
    return conn.execute(
        UPDATE_RESUME_SQL, (type_id, version, name, resume_id)
    ).fetchone()


def delete(conn: sqlite3.Connection, resume_id: int) -> sqlite3.Row:
    return conn.execute(DELETE_RESUME_SQL, (resume_id,)).fetchone()
