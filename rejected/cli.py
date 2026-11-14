import typer
from database import transaction
from error import ResourceNotFoundError
from rich.console import Console
from rich.table import Table
from service import application_service

app = typer.Typer()


@app.command()
def add(company: str, role: str, source: str = "other"):
    print("Adding application", company, role, source)


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
            application.applied_at.strftime("%m/%d/%Y"),
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
def update(application_id: str):
    print("Updating application", application_id)
