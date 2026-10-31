import sqlite3
from typing import Optional

from models.application import Application

FIND_APPLICATION_SQL = """
    SELECT *
    FROM applications
    WHERE id = ?
"""

FIND_APPLICATION_BY_COMPANY_AND_ROLE_SQL = """
    SELECT *
    FROM applications
    WHERE company = ?
    AND role = ?
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


def find(conn: sqlite3.Connection, application_id: int) -> Optional[Application]:
    row = conn.execute(
        FIND_APPLICATION_SQL,
        (application_id,),
    ).fetchone()
    return Application(**dict(row)) if row else None


def find_by_company_and_role(
    conn: sqlite3.Connection, company: str, role: str
) -> Optional[Application]:
    row = conn.execute(
        FIND_APPLICATION_BY_COMPANY_AND_ROLE_SQL,
        (
            company,
            role,
        ),
    ).fetchone()
    return Application(**dict(row)) if row else None


def find_all(conn: sqlite3.Connection) -> list[Application]:
    rows = conn.execute(FIND_ALL_APPLICATIONS_SQL).fetchall()
    return [Application(**dict(row)) for row in rows]


def insert(
    conn: sqlite3.Connection,
    company: str,
    role: str,
    applied_at: str,
    resume_type_id: int = None,
    source: str = None,
) -> Optional[Application]:
    row = conn.execute(
        INSERT_APPLICATION_SQL,
        (company, role, applied_at, resume_type_id, source),
    ).fetchone()
    return Application(**dict(row)) if row else None


def update(
    conn: sqlite3.Connection,
    application_id: int,
    company: str,
    role: str,
    applied_at: str,
    resume_type_id: int,
    source: str,
) -> Optional[Application]:
    row = conn.execute(
        UPDATE_APPLICATION_SQL,
        (company, role, applied_at, resume_type_id, source, application_id),
    ).fetchone()
    return Application(**dict(row)) if row else None


def delete(conn: sqlite3.Connection, application_id: int) -> bool:
    cursor = conn.execute(
        DELETE_APPLICATION_SQL,
        (application_id,),
    )
    return cursor.rowcount > 0
