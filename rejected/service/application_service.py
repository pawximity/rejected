import sqlite3

import repository.application_repository as application_repository
import repository.resume_type_repository as resume_type_repository
from error import ResourceNotFoundError
from models.application import Application
from models.application_event import ApplicationEvent
from models.application_event_types import ApplicationEventType
from repository import application_event_repository


def list_applications(conn: sqlite3.Connection) -> list[Application]:
    applications = application_repository.find_all(conn)
    if not applications:
        raise ResourceNotFoundError("No applications found")
    return applications


def get_applications_by_company(
    conn: sqlite3.Connection, company: str
) -> list[Application]:
    applications = application_repository.find_by_company(conn, company)
    if not applications:
        raise ResourceNotFoundError(f"No applications found for {company}")
    return applications


def create_application(
    conn: sqlite3.Connection,
    company: str,
    role: str,
    applied_at: str,
    resume_type_name: str,
    source: str = None,
) -> Application:
    resume_type = resume_type_repository.find_by_name(conn, resume_type_name)
    if resume_type is None:
        raise ResourceNotFoundError(f"Resume type not found: {resume_type_name}")
    application = application_repository.insert(
        conn, company, role, applied_at, resume_type.id, source
    )
    if application is None:
        raise RuntimeError(f"Failed to create application for {role} at {company}")
    return application


def create_event(
    conn: sqlite3.Connection,
    application_id: int,
    company: str,
    role: str,
    event_type: ApplicationEventType,
    occurred_at: str,
    notes: str = None,
) -> ApplicationEvent:
    application = application_repository.find(conn, application_id)
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
