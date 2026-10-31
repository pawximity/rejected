import sqlite3

FIND_APPLICATION_SQL = """
    SELECT *
    FROM applications
    WHERE id = ?
"""

FIND_ALL_APPLICATIONS_SQL = """
    SELECT *
    FROM applications
    ORDER BY applied_at DESC, id DESC
"""

INSERT_APPLICATION_SQL = """
    INSERT INTO applications (
        company, role, applied_at, resume_type_id, source
    )
    VALUES (?, ?, ?, ?, ?)
    RETURNING *
"""

UPDATE_APPLICATION_SQL = """
    UPDATE applications
    SET company = ?,
        role = ?,
        applied_at = ?,
        resume_type_id = ?,
        source = ?,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = ?
    RETURNING *
"""

DELETE_APPLICATION_SQL = """
    DELETE FROM applications
    WHERE id = ?
"""


def find(conn: sqlite3.Connection, application_id: int) -> sqlite3.Row:
    return conn.execute(
        FIND_APPLICATION_SQL,
        (application_id,),
    ).fetchone()


def find_all(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute(FIND_ALL_APPLICATIONS_SQL).fetchall()


def insert(
    conn: sqlite3.Connection,
    company: str,
    role: str,
    applied_at: str,
    resume_type_id: int = None,
    source: str = None,
) -> sqlite3.Row:
    return conn.execute(
        INSERT_APPLICATION_SQL,
        (company, role, applied_at, resume_type_id, source),
    ).fetchone()


def update(
    conn: sqlite3.Connection,
    application_id: int,
    company: str,
    role: str,
    applied_at: str,
    resume_type_id: int,
    source: str,
) -> sqlite3.Row:
    return conn.execute(
        UPDATE_APPLICATION_SQL,
        (company, role, applied_at, resume_type_id, source, application_id),
    ).fetchone()


def delete(conn: sqlite3.Connection, application_id: int) -> bool:
    cursor = conn.execute(
        DELETE_APPLICATION_SQL,
        (application_id,),
    )
    return cursor.rowcount > 0
