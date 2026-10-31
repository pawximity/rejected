import sqlite3

import repository.resume_type_repository as resume_type_repository
from models.resume_type import ResumeType


def get_resume_type_by_name(conn: sqlite3.Connection, name: str) -> ResumeType:
    row = resume_type_repository.find_by_name(conn, name)
    return ResumeType(**dict(row))


def get_resume_types(conn: sqlite3.Connection) -> list[ResumeType]:
    rows = resume_type_repository.find_all(conn)
    return [ResumeType(**dict(row)) for row in rows]


def create_resume_type(conn: sqlite3.Connection, name: str) -> ResumeType:
    row = resume_type_repository.insert(conn, name)
    return ResumeType(**dict(row))
