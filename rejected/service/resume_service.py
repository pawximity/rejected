import sqlite3

import repository.resume_type_repository as resume_type_repository
from models import resume_type
from models.resume_categories import ResumeCategory


def create_resume_type(conn: sqlite3.Connection, category_name: ResumeCategory):
    with conn:
        row = resume_type_repository.insert(conn, category_name.value)
        return resume_type.ResumeType(**dict(row))