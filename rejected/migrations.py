import sqlite3

CREATE_RESUME_TYPES_TABLE = """
    CREATE TABLE resume_types (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
"""

CREATE_RESUMES_TABLE = """
    CREATE TABLE resumes (
        id INTEGER PRIMARY KEY,
        type_id INTEGER NOT NULL,
        version INTEGER NOT NULL CHECK (version > 0),
        name TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (type_id) REFERENCES resume_types(id),
        UNIQUE (type_id, version)
    )
"""

CREATE_APPLICATIONS_TABLE = """
    CREATE TABLE applications (
        id INTEGER PRIMARY KEY,
        company TEXT NOT NULL,
        role TEXT NOT NULL,
        applied_at TEXT NOT NULL,
        resume_id INTEGER,
        source TEXT,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (resume_id) REFERENCES resumes(id)
    )
"""

CREATE_APPLICATION_EVENTS_TABLE = """
    CREATE TABLE application_events (
        id INTEGER PRIMARY KEY,
        application_id INTEGER NOT NULL,
        event_type TEXT NOT NULL,
        occurred_at TEXT NOT NULL,
        notes TEXT,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (application_id) REFERENCES applications(id)
    )
"""

CREATE_APPLICATION_EVENTS_INDEX = """
    CREATE INDEX idx_events_application ON application_events(application_id)
"""

CREATE_RESUMES_TYPE_INDEX = """
    CREATE INDEX idx_resumes_type ON resumes(type_id)
"""

CREATE_APPLICATION_RESUME_INDEX = """
    CREATE INDEX idx_applications_resume ON applications(resume_id);
"""


def migration_001(conn: sqlite3.Connection) -> None:
    conn.execute(CREATE_RESUME_TYPES_TABLE)


def migration_002(conn: sqlite3.Connection) -> None:
    conn.execute(CREATE_RESUMES_TABLE)
    conn.execute(CREATE_RESUMES_TYPE_INDEX)


def migration_003(conn: sqlite3.Connection) -> None:
    conn.execute(CREATE_APPLICATIONS_TABLE)
    conn.execute(CREATE_APPLICATION_RESUME_INDEX)


def migration_004(conn: sqlite3.Connection) -> None:
    conn.execute(CREATE_APPLICATION_EVENTS_TABLE)
    conn.execute(CREATE_APPLICATION_EVENTS_INDEX)


MIGRATIONS = {
    1: migration_001,
    2: migration_002,
    3: migration_003,
    4: migration_004,
}


def migrate(conn: sqlite3.Connection) -> None:
    current_version = conn.execute(
        "PRAGMA user_version"
    ).fetchone()[0]

    latest_version = max(MIGRATIONS)
    if current_version > latest_version:
        raise RuntimeError(
            f"Database version {current_version} "
            f"is newer than supported version {latest_version}"
        )

    for version in range(current_version + 1, latest_version + 1):
        print(f"Applying migration {version}")
        conn.execute("BEGIN IMMEDIATE")
        try:
            MIGRATIONS[version](conn)
            conn.execute(
                f"PRAGMA user_version = {version}"
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
