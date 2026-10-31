import sqlite3

import repository.application_repository as application_repository
import repository.resume_type_repository as resume_type_repository
from error import ResourceNotFoundError
from models.application import Application
from models.application_event import ApplicationEvent
from models.application_event_types import ApplicationEventType
from models.resume_categories import ResumeCategory
from repository import application_event_repository


def create_application(
    conn: sqlite3.Connection,
    company: str,
    role: str,
    applied_at: str,
    resume_category: ResumeCategory,
    source: str = None,
) -> Application:
    resume_type = resume_type_repository.find_by_name(conn, resume_category.value)
    if resume_type is None:
        raise ResourceNotFoundError(f"Resume type not found: {resume_category.value}")
    application = application_repository.insert(
        conn, company, role, applied_at, resume_type.id, source
    )
    if application is None:
        raise RuntimeError(f"Failed to create application for {role} at {company}")
    return application


def create_event(
    conn: sqlite3.Connection,
    company: str,
    role: str,
    event_type: ApplicationEventType,
    occurred_at: str,
    notes: str = None,
) -> ApplicationEvent:
    application = application_repository.find_by_company_and_role(conn, company, role)
    if application is None:
        raise ResourceNotFoundError(f"Application not found for {role} at {company}")
    event = application_event_repository.insert(
        conn, application.id, event_type.value, occurred_at, notes
    )
    if event is None:
        raise RuntimeError(
            f"Failed to create {event_type.value} event for {role} at {company}"
        )
    return event
