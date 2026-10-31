import sqlite3

import repository.application_repository as application_repository
import service.resume_service as resume_service
from models.application import Application
from models.resume_categories import ResumeCategory


def create_application(
    conn: sqlite3.Connection,
    company: str,
    role: str,
    applied_at: str,
    resume_category: ResumeCategory,
    source: str = None,
) -> Application:
    resume_type = resume_service.get_resume_type_by_name(conn, resume_category.name)
    if not resume_type:
        resume_type = resume_service.create_resume_type(conn, resume_category.name)
    row = application_repository.insert(
        conn, company, role, applied_at, resume_type.id, source
    )
    return Application(**row)
