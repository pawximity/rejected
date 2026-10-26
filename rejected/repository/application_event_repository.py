import sqlite3

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


def find(conn: sqlite3.Connection, application_event_id: int) -> sqlite3.Row:
    return conn.execute(
        FIND_APPLICATION_EVENT_SQL,
        (application_event_id,),
    ).fetchone()


def find_all(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute(FIND_ALL_APPLICATION_EVENTS_SQL).fetchall()


def insert(
    conn: sqlite3.Connection,
    application_id: int,
    event_type: str,
    occurred_at: str,
    notes: str = None,
) -> sqlite3.Row:
    return conn.execute(
        INSERT_APPLICATION_EVENT_SQL,
        (application_id, event_type, occurred_at, notes),
    ).fetchone()


def update(
    conn: sqlite3.Connection,
    application_event_id: int,
    application_id: int,
    event_type: str,
    occurred_at: str,
    notes: str = None,
) -> sqlite3.Row:
    return conn.execute(
        UPDATE_APPLICATION_EVENT_SQL,
        (application_id, event_type, occurred_at, notes, application_event_id),
    ).fetchone()


def delete(conn: sqlite3.Connection, application_event_id: int) -> bool:
    cursor = conn.execute(
        DELETE_APPLICATION_EVENT_SQL,
        (application_event_id,),
    )
    return cursor.rowcount > 0
