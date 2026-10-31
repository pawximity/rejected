import sqlite3
from typing import Optional

from models.resume_type import ResumeType

FIND_RESUME_TYPE_SQL = """
    SELECT *
    FROM resume_types
    WHERE id = ?
"""

FIND_RESUME_TYPE_BY_NAME_SQL = """
    SELECT *
    FROM resume_types
    WHERE name = ?
"""

FIND_ALL_RESUME_TYPES_SQL = """
    SELECT *
    FROM resume_types
    ORDER BY created_at DESC
"""

INSERT_RESUME_TYPE_SQL = """
    INSERT INTO resume_types (
        name
    )
    VALUES (?)
    RETURNING *
"""

UPDATE_RESUME_TYPE_SQL = """
    UPDATE resume_types
    SET name = ?,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = ?
    RETURNING *
"""

DELETE_RESUME_TYPE_SQL = """
    DELETE FROM resume_types
    WHERE id = ?
"""


def find(conn: sqlite3.Connection, resume_type_id: int) -> Optional[ResumeType]:
    row = conn.execute(FIND_RESUME_TYPE_SQL, (resume_type_id,)).fetchone()
    return ResumeType(**dict(row)) if row else None


def find_by_name(conn: sqlite3.Connection, name: str) -> Optional[ResumeType]:
    row = conn.execute(FIND_RESUME_TYPE_BY_NAME_SQL, (name,)).fetchone()
    return ResumeType(**dict(row)) if row else None


def find_all(conn: sqlite3.Connection) -> list[ResumeType]:
    rows = conn.execute(FIND_ALL_RESUME_TYPES_SQL).fetchall()
    return [ResumeType(**dict(row)) for row in rows]


def insert(conn: sqlite3.Connection, name: str) -> Optional[ResumeType]:
    row = conn.execute(INSERT_RESUME_TYPE_SQL, (name,)).fetchone()
    return ResumeType(**dict(row)) if row else None


def update(
    conn: sqlite3.Connection,
    resume_type_id: int,
    name: str,
) -> Optional[ResumeType]:
    row = conn.execute(UPDATE_RESUME_TYPE_SQL, (name, resume_type_id)).fetchone()
    return ResumeType(**dict(row)) if row else None


def delete(conn: sqlite3.Connection, resume_type_id: int) -> bool:
    cursor = conn.execute(
        DELETE_RESUME_TYPE_SQL,
        (resume_type_id,),
    )
    return cursor.rowcount > 0
