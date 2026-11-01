import sqlite3

import repository.resume_type_repository as resume_type_repository
from error import ResourceNotFoundError, ValidationError
from models.resume_type import ResumeType


def list_resume_types(conn: sqlite3.Connection) -> list[ResumeType]:
    resume_types = resume_type_repository.find_all(conn)
    if not resume_types:
        raise ResourceNotFoundError("No resume types found")
    return resume_types


def create_resume_type(conn: sqlite3.Connection, resume_type_name: str) -> ResumeType:
    existing_resume_type = resume_type_repository.find_by_name(conn, resume_type_name)
    if existing_resume_type:
        raise ValidationError(
            f"Resume type with name {resume_type_name} already exists"
        )
    resume_type = resume_type_repository.insert(conn, resume_type_name)
    if resume_type is None:
        raise RuntimeError(f"Failed to create resume type {resume_type_name}")
    return resume_type
