import sqlite3
from typing import Optional

from models.application_event import ApplicationEvent

FIND_APPLICATION_EVENT_SQL = """
    SELECT *
    FROM application_events
    WHERE id = ?
"""

FIND_ALL_APPLICATION_EVENTS_SQL = """
    SELECT *
    FROM application_events
    ORDER BY occurred_at DESC
"""

FIND_ALL_APPLICATION_EVENTS_BY_COMPANY = """
    SELECT ae.*
    FROM application_events ae
    JOIN applications a
    ON ae.application_id = a.id
    WHERE a.company = ?
"""

INSERT_APPLICATION_EVENT_SQL = """
    INSERT INTO application_events (
        application_id, event_type, occurred_at, notes
    )
    VALUES (?, ?, ?, ?)
    RETURNING *
"""

UPDATE_APPLICATION_EVENT_SQL = """
    UPDATE application_events
    SET application_id = ?,
        event_type = ?,
        occurred_at = ?,
        notes = ?
        updated_at = CURRENT_TIMESTAMP
    WHERE id = ?
    RETURNING *
"""

DELETE_APPLICATION_EVENT_SQL = """
    DELETE FROM application_events
    WHERE id = ?
"""


def find(
    conn: sqlite3.Connection, application_event_id: int
) -> Optional[ApplicationEvent]:
    row = conn.execute(
        FIND_APPLICATION_EVENT_SQL,
        (application_event_id,),
    ).fetchone()
    return ApplicationEvent(**dict(row)) if row else None


def find_all(conn: sqlite3.Connection) -> list[ApplicationEvent]:
    rows = conn.execute(FIND_ALL_APPLICATION_EVENTS_SQL).fetchall()
    return [ApplicationEvent(**dict(row)) for row in rows]


def find_by_company(conn: sqlite3.Connection, company: str) -> list[ApplicationEvent]:
    rows = conn.execute(FIND_ALL_APPLICATION_EVENTS_BY_COMPANY, (company,)).fetchall()
    return [ApplicationEvent(**dict(row)) for row in rows]


def insert(
    conn: sqlite3.Connection,
    application_id: int,
    event_type: str,
    occurred_at: str,
    notes: str = None,
) -> Optional[ApplicationEvent]:
    row = conn.execute(
        INSERT_APPLICATION_EVENT_SQL,
        (application_id, event_type, occurred_at, notes),
    ).fetchone()
    return ApplicationEvent(**dict(row)) if row else None


def update(
    conn: sqlite3.Connection,
    application_event_id: int,
    application_id: int,
    event_type: str,
    occurred_at: str,
    notes: str = None,
) -> Optional[ApplicationEvent]:
    row = conn.execute(
        UPDATE_APPLICATION_EVENT_SQL,
        (application_id, event_type, occurred_at, notes, application_event_id),
    ).fetchone()
    return ApplicationEvent(**dict(row)) if row else None


def delete(conn: sqlite3.Connection, application_event_id: int) -> bool:
    cursor = conn.execute(
        DELETE_APPLICATION_EVENT_SQL,
        (application_event_id,),
    )
    return cursor.rowcount > 0
