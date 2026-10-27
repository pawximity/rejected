import sqlite3
from importlib.abc import Traversable
from importlib.resources import files


def migrate(conn: sqlite3.Connection) -> None:
    migrations = find_migrations()

    current_version = conn.execute("PRAGMA user_version").fetchone()[0]

    latest_version = migrations[-1][0] if migrations else 0
    if current_version > latest_version:
        raise RuntimeError(
            f"Database version {current_version} "
            f"is newer than supported version {latest_version}"
        )

    for version, path in migrations:
        if version <= current_version:
            continue
        sql = path.read_text(encoding="utf-8")
        script = migration_script_format(sql, version)
        try:
            conn.executescript(script)
        except Exception:
            if conn.in_transaction:
                conn.rollback()
            raise


def find_migrations() -> list[tuple[int, Traversable]]:
    migration_dir = files("rejected").joinpath("sql")
    migrations = []
    for path in migration_dir.iterdir():
        if path.name.endswith(".sql"):
            version = int(path.name.split("_", 1)[0])
            migrations.append((version, path))

    migrations.sort(key=lambda migration: migration[0])
    versions = [version for version, _ in migrations]
    if versions != list(range(1, len(versions) + 1)):
        raise RuntimeError(f"Invalid migration sequence: {versions}")
    return migrations


def migration_script_format(sql: str, version: int) -> str:
    return f"""
            BEGIN IMMEDIATE;

            {sql}

            PRAGMA user_version = {version};

            COMMIT;
            """
