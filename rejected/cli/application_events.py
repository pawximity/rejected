import typer
from database import transaction
from error import ResourceNotFoundError, ValidationError
from rich.console import Console
from rich.table import Table
from service import application_service

app = typer.Typer()
console = Console()


@app.command()
def add(
    application_id: str,
    company: str,
    role: str,
    event_type: str,
    occurred_at: str,
    notes: str = None,
):
    try:
        with transaction() as conn:
            application_event = application_service.create_event(
                conn, int(application_id), company, role, event_type, occurred_at, notes
            )
    except (ResourceNotFoundError, ValidationError, RuntimeError) as e:
        console.print(f"Error: {e}")
        raise typer.Exit(code=1) from e

    console.print("Successfully created application event", application_event.id)


@app.command()
def list():
    try:
        with transaction() as conn:
            application_events = application_service.list_events(conn)
    except ResourceNotFoundError as e:
        console.print(f"Error: {e}")
        raise typer.Exit(code=1) from e

    table = Table(title="Application Events")
    table.add_column("ID")
    table.add_column("Application ID")
    table.add_column("Event Type")
    table.add_column("Occurred At")
    table.add_column("Notes")

    for application_event in application_events:
        table.add_row(
            str(application_event.id),
            str(application_event.application_id),
            application_event.event_type,
            application_event.occurred_at,
            application_event.notes,
        )

    console.print(table)
