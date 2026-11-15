import typer
from database import transaction
from error import ResourceNotFoundError, ValidationError
from rich.console import Console
from rich.table import Table
from service import application_service

app = typer.Typer()


@app.command()
def add(
    company: str, role: str, applied_at: str, resume_type: str, source: str = "other"
):
    try:
        with transaction() as conn:
            application = application_service.create_application(
                conn, company, role, applied_at, resume_type, source
            )
    except (ResourceNotFoundError, ValidationError) as e:
        Console().print(f"Error: {e}")
        raise typer.Exit(code=1) from e

    Console().print("Successfully created application", application.id)


@app.command()
def list():
    try:
        with transaction() as conn:
            applications = application_service.list_applications(conn)
    except ResourceNotFoundError as e:
        Console().print(f"Error: {e}")
        raise typer.Exit(code=1) from e

    table = Table(title="Applications")
    table.add_column("ID")
    table.add_column("Company")
    table.add_column("Role")
    table.add_column("Applied")
    table.add_column("Resume Type ID")

    for application in applications:
        table.add_row(
            str(application.id),
            application.company,
            application.role,
            application.applied_at,
            str(application.resume_type_id or "-"),
        )

    Console().print(table)


@app.command()
def remove(application_id: str):
    try:
        with transaction() as conn:
            application_service.remove_application(conn, int(application_id))
    except ResourceNotFoundError as e:
        Console().print(f"Error: {e}")
        raise typer.Exit(code=1) from e

    Console().print("Successfully removed application", application_id)


@app.command()
def update(
    application_id: str,
    company: str,
    role: str,
    applied_at: str,
    resume_type: str,
    source: str = "other",
):
    try:
        with transaction() as conn:
            updated_application = application_service.update_application(
                conn,
                int(application_id),
                company,
                role,
                applied_at,
                resume_type,
                source,
            )
    except (ResourceNotFoundError, ValidationError) as e:
        Console().print(f"Error: {e}")
        raise typer.Exit(code=1) from e

    Console().print("Successfully updated application", updated_application.id)
